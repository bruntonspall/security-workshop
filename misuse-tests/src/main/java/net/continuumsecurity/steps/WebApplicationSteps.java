/*******************************************************************************
 *    BDD-Security, application security testing framework
 *
 * Copyright (C) `2014 Stephen de Vries`
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see `<http://www.gnu.org/licenses/>`.
 ******************************************************************************/
package net.continuumsecurity.steps;

import edu.umass.cs.benchlab.har.HarCookie;
import edu.umass.cs.benchlab.har.HarEntry;
import edu.umass.cs.benchlab.har.HarRequest;
import net.continuumsecurity.*;
import net.continuumsecurity.behaviour.ICaptcha;
import net.continuumsecurity.behaviour.ILogin;
import net.continuumsecurity.behaviour.ILogout;
import net.continuumsecurity.behaviour.IRecoverPassword;
import net.continuumsecurity.proxy.LoggingProxy;
import net.continuumsecurity.proxy.ZAProxyScanner;
import net.continuumsecurity.web.Application;
import net.continuumsecurity.web.FakeCaptchaSolver;
import net.continuumsecurity.web.StepException;
import net.continuumsecurity.web.WebApplication;
import org.apache.log4j.Logger;
import org.jbehave.core.annotations.*;
import org.jbehave.core.model.ExamplesTable;
import org.openqa.selenium.By;
import org.openqa.selenium.Cookie;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.WebDriver;
import sun.net.www.http.HttpClient;


import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static junit.framework.TestCase.assertNotNull;
import static net.continuumsecurity.Utils.countInstances;
import static net.continuumsecurity.Utils.executePost;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;
import static org.junit.Assert.fail;

public class WebApplicationSteps {
    Logger log = Logger.getLogger(WebApplicationSteps.class);
    public Application app;
    UserPassCredentials credentials;
    WebDriver driver;

    public static final String GOOD_SORTCODE = "123456";
    public static final String GOOD_ACCOUNT = "12437856";
    public static final String HACKER_SORTCODE = "606060";
    public static final String HACKER_ACCOUNT = "98765432";


    public WebApplicationSteps() {

    }

    @BeforeStories
    public void beforeStories() {
        Config.getInstance().initialiseTables();
    }
    /*
     * This has to be called explicitly when using an examples table in order to
     * start with a fresh browser instance, because @BeforeScenario is only
     * called once for the whole scenario, not each example.
     */
    public void createApp() {
        app = Config.getInstance().createApp();
        app.enableDefaultClient();
        driver = app.getWebDriver();
        driver.manage().deleteAllCookies();
        credentials = new UserPassCredentials("", "");
        driver.get("http://localhost:8081/setup");
        driver.get("http://localhost:8082/setup");

    }


    @Given("the login page")
    @When("the login page is displayed")
    public void openLoginPage() {
        ((ILogin) app).openLoginPage();
    }

    @When("the user logs in")
    @Given("the user logs in")
    public void loginWithSetCredentials() {
        assert credentials != null;
        ((ILogin) app).login(credentials);
    }

    @Given("the system contains a claim")
    public void theSystemContainsAClaim() {
        createApp();
        ((ILogin)app).openLoginPage();
        ((ILogin)app).login(new UserPassCredentials("admin", "password1"));
        driver.findElement(By.id("sortcode")).clear();
        driver.findElement(By.id("sortcode")).sendKeys(GOOD_SORTCODE);
        driver.findElement(By.id("account")).clear();
        driver.findElement(By.id("account")).sendKeys(GOOD_ACCOUNT);
        driver.findElement(By.id("update")).click();

        driver.findElement(By.id("claim")).click();
    }
    @When("a hacker requests data from the payments api using a username")
    public void requestAdminsDetailsFromPaymentsApi() {
        driver.get("http://localhost:8082/account/admin");
    }

    @Then("the users bank details should not be returned")
    public void AdminsDetailsShouldBeReturned() {
        assertThat(driver.getPageSource(), not(containsString(HACKER_SORTCODE)));
        assertThat(driver.getPageSource(), not(containsString(HACKER_ACCOUNT)));
    }

    String response = null;

    @When("a hacker posts their bank details to the payments api using a username")
    public void postBankDetails() throws Exception {
        // Use a HTTP Client to post to the API
        String params = "sortcode="+URLEncoder.encode(HACKER_SORTCODE, "UTF-8")+
                "&accountnumber="+URLEncoder.encode(HACKER_ACCOUNT, "UTF-8");
        response = executePost("http://localhost:8082/account/admin", params);
    }

    @Then("the payment should not be sent to the criminal")
    public void checkBankDetails() {
        assertThat(response.contains("987654"), is(false));
        assertThat(response.contains("87654321"), is(false));
    }

    @When("a fraudster posts a duplicate bank details claim")
    public void fraudulantlyMakeAClaim() {
        // Repeat the good sortcode
        ((ILogin)app).openLoginPage();
        ((ILogin)app).login(new UserPassCredentials("anna", "letmein1"));
        driver.findElement(By.id("sortcode")).clear();
        driver.findElement(By.id("sortcode")).sendKeys(GOOD_SORTCODE);
        driver.findElement(By.id("account")).clear();
        driver.findElement(By.id("account")).sendKeys(GOOD_ACCOUNT);
        driver.findElement(By.id("update")).click();
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {

        }

        // Once the details are submitted, the claim button should still not appear
        boolean thrown = false;
        try {
            driver.findElement(By.id("claim"));
        } catch (NoSuchElementException e) {
            thrown = true;
        }
        assertThat(thrown, is(true));
    }

    @Then("the second claim should not be paid")
    public void checkSecondClaimIsNotPaid() {
        driver.get("http://localhost:8082/payments");
        String src = driver.getPageSource();
        assertThat(countInstances(src, GOOD_ACCOUNT), equalTo(1));
        assertThat(countInstances(src, GOOD_SORTCODE), equalTo(1));
    }

}

