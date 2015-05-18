package net.continuumsecurity;

import net.continuumsecurity.Config;
import net.continuumsecurity.Credentials;
import net.continuumsecurity.Restricted;
import net.continuumsecurity.UserPassCredentials;
import net.continuumsecurity.behaviour.ICaptcha;
import net.continuumsecurity.behaviour.ILogin;
import net.continuumsecurity.behaviour.ILogout;
import net.continuumsecurity.behaviour.IRecoverPassword;
import net.continuumsecurity.web.CaptchaSolver;
import net.continuumsecurity.web.WebApplication;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Map;
import java.util.Properties;

public class WorkshopTasksApplication extends WebApplication implements ILogin,
        ILogout {
    @Override
    public void openLoginPage() {
        driver.get(Config.getInstance().getBaseUrl() + "/");
        verifyTextPresent("Welcome");
    }

    @Override
    public void login(Credentials credentials) {
        UserPassCredentials creds = new UserPassCredentials(credentials);
        driver.findElement(By.id("username")).clear();
        driver.findElement(By.id("username")).sendKeys(creds.getUsername());
        driver.findElement(By.id("password")).clear();
        driver.findElement(By.id("password")).sendKeys(creds.getPassword());
        driver.findElement(By.id("login")).click();
    }

    // Convenience method
    public void login(String username, String password) {
        login(new UserPassCredentials(username, password));
    }

    @Override
    public boolean isLoggedIn() {
        if (driver.getPageSource().contains("Your bank details")) {
            return true;
        } else {
            return false;
        }
    }

    // App Specific methods
    public void updateBankDetails() {
        driver.findElement(By.id("sortcode")).clear();
        driver.findElement(By.id("sortcode")).sendKeys("102030");
        driver.findElement(By.id("account")).clear();
        driver.findElement(By.id("account")).sendKeys("12345678");
        driver.findElement(By.id("update")).click();
    }

    public void claimPayment() {
        driver.findElement(By.id("claim")).click();
    }
    public void navigate() {
        openLoginPage();
        login(Config.getInstance().getUsers().getDefaultCredentials());
        verifyTextPresent("Your bank details");
        updateBankDetails();
        claimPayment();
    }


    @Override
    public void logout() {
        driver.findElement(By.linkText("Logout")).click();
    }

}