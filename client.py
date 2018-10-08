from __future__ import print_function
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains



def get_date_time():
    """
    get the full date along with the hour of the search, just for 
    completeness. Allows us to solve for of the original post 
    date.
    """
    now   =  datetime.datetime.now()
    month =  str(now.month) if now.month > 9 else '0' + str(now.month)
    day   =  str(now.day) if now.day > 9 else '0' + str(now.day)
    date  =  ''.join(str(t) for t in [now.year, month, day, now.time().hour])
    return date





def robust_wait_for_clickable_element(driver, delay, selector):
    """ wait for css selector to load """
    clickable = False
    attempts = 1
    try:
        driver.find_element_by_xpath(selector)
    except Exception as e:
        print("  Selector not found: {}".format(selector))
    else:
        while not clickable:
            try:
                # wait for job post link to load
                wait_for_clickable_element(driver, delay, selector)
            except Exception as e:
                print("  {}".format(e))
                attempts += 1
                if attempts % 100 == 0:
                    driver.refresh()
                if attempts > 10**3: 
                    print("  \nrobust_wait_for_clickable_element failed " \
                                    "after too many attempts\n")
                    break
                pass
            else:
                clickable = True

def robust_click(driver, delay, selector):
    """
    use a while-looop to click an element. For stubborn links
    and general unexpected browser errors.
    """
    try:
        driver.find_element_by_xpath(selector).click()
    except Exception as e:
        print("  The job post link was likely hidden,\n    An " \
                "error was encountered while attempting to click link" \
                "\n    {}".format(e))
        attempts = 1
        clicked = False
        while not clicked:
            try:
                driver.find_element_by_xpath(selector).click()
            except Exception as e:
                pass
            else:
                clicked = True
                print("  Successfully navigated to job post page "\
                            "after {} attempts".format(attempts))
            finally:
                attempts += 1
                if attempts % 100 == 0:
                    print("--------------  refreshing page")
                    driver.refresh()
                    time.sleep(5)
                if attempts > 10**3:
                    print(selector)
                    print("  robust_click method failed after too many attempts")
                    break 


def wait_for_clickable_element(driver, delay, selector):
    """use WebDriverWait to wait for an element to become clickable"""
    obj = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable(
                (By.XPATH, selector)
            )
        )
    return obj  

def wait_for_clickable_element_css(driver, delay, selector):
    """use WebDriverWait to wait for an element to become clickable"""
    obj = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, selector)
            )
        )
    return obj  


def link_is_present(driver, delay, selector, index, results_page):
    """
    verify that the link selector is present and print the search 
    details to console. This method is particularly useful for catching
    the last link on the last page of search results
    """
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located(
                (By.XPATH, selector)
            )
        )
        print("**************************************************")
        print("\nScraping data for result  {}" \
                "  on results page  {} \n".format(index, results_page))
    except Exception as e:
        print(e)
        if index < 25:
            print("\nWas not able to wait for job_selector to load. Search " \
                    "results may have been exhausted.")
            return True
        else:
            return False
    else:
        return True 


def search_suggestion_box_is_present(driver, selector, index, results_page):
    """
    check results page for the search suggestion box,
    as this causes some errors in navigate search results.
    """
    if (index == 1) and (results_page == 1):
        try:
            # This try-except statement allows us to avoid the 
            # problems cause by the LinkedIn search suggestion box
            driver.find_element_by_css_selector("div.suggested-search.bd")
        except Exception as e:
            pass
        else:
            return True
    else:
        return False

def next_results_page(driver, delay):
    """
    navigate to the next page of search results. If an error is encountered
    then the process ends or new search criteria are entered as the current 
    search results may have been exhausted.
    """
    try:
        
        # wait for the next page button to load
        #print("  Moving to the next page of search results... \n" \
        #        "  If search results are exhausted, will wait {} seconds " \
        #        "then either execute new search or quit".format(delay))
        wait_for_clickable_element_css(driver, delay, "button.next")
        # navigate to next page
        driver.find_element_by_css_selector("button.next").click()
        print("["+str(datetime.datetime.now())+"] Pobieram dane z kolejnej strony wynikow")
        return False
    except Exception as e:
        print("["+str(datetime.datetime.now())+"] Koniec wynikow")
        return True
        #print ("\nFailed to click next page link; Search results " \
        #                        "may have been exhausted\n{}".format(e))
        #raise ValueError("Next page link not detected; search results exhausted")
        
    else:
        time.sleep(0.5)
        # wait until the first job post button has loaded
        #first_job_button = "a.job-title-link"
        # wait for the first job post button to load
        #wait_for_clickable_element_css(driver, delay, first_job_button)

def go_to_specific_results_page(driver, delay, results_page):
    """
    go to a specific results page in case of an error, can restart 
    the webdriver where the error occurred.
    """
    if results_page < 2:
        return
    current_page = 1
    for i in range(results_page):
        current_page += 1
        time.sleep(0.5)
        try:
            next_results_page(driver, delay)
        except ValueError:
            pass


def print_num_search_results(driver, keyword, location):
    """print the number of search results to console"""
    # scroll to top of page so first result is in view
    driver.execute_script("window.scrollTo(0, 0);")
    selector = "div.results-context div strong"
    try:
        num_results = driver.find_element_by_css_selector(selector).text
    except Exception as e:
        num_results = ''
    #print("**************************************************")
    #print("\n\n\n\n\nSearching  {}  results for  '{}'  jobs in  '{}' " \
    #       "\n\n\n\n\n".format(num_results, keyword, location))



class LIClient(object):
    def __init__(self, driver):
        self.driver  =  driver
        self.results_page = 1
        self.data   = json.load(open('query.json', 'r'))

    def driver_quit(self):
        self.driver.quit()
        
    def login(self):
        """login to linkedin then wait 3 seconds for page to load"""
        
        # Enter login credentials
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable( (By.ID, "session_key-login")))
        
        self.driver.find_element_by_id("session_key-login").send_keys(self.data["username"])
        self.driver.find_element_by_id("session_password-login").send_keys(self.data["password"]+Keys.RETURN)
        time.sleep(2)

    def navigate_to_jobs_page(self):

        try:
            self.driver.get("https://www.linkedin.com/jobs/search")
        except Exception as e: 
            print("here comes logging: failed to navigate to jobs page")

    def enter_search_keys(self):
        """
        execute the job search by entering job and location information.
        The location is pre-filled with text, so we must clear it before
        entering our search.
        """

        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR , "input[id^=jobs-search-box-keyword-id-ember]")))  
        
        self.driver.find_element_by_css_selector("input[id^=jobs-search-box-keyword-id-ember]").send_keys(self.data["position"])
        self.driver.find_element_by_css_selector("input[id^=jobs-search-box-location-id-ember]").clear()
        self.driver.find_element_by_css_selector("input[id^=jobs-search-box-location-id-ember]").send_keys(self.data["location"]+Keys.RETURN)
        time.sleep(1)

    def adjust_results_view(self):
        menus = self.driver.find_elements_by_css_selector("button.jobs-search-dropdown__trigger")
        menus[1].click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("button.jobs-search-dropdown__option-button--single").click()
        self.driver.find_element_by_css_selector("[aria-controls=date-posted-facet-values]").click()
        time.sleep(0.2)
        self.driver.find_element_by_css_selector("input[value='1,2'] + label.search-s-facet-value__label").click()
        time.sleep(0.2)
        self.driver.find_element_by_css_selector("button[data-control-name=filter_pill_apply]").click()
        time.sleep(0.2)
    
    def scrape_all_links(self):
        ''' naaaa, lets jsut leave it as "in progress" '''
        all_links = []
        visible_link_elements = []
        done = False
        
        while not done:
            
            visible_link_elements = self.driver.find_elements_by_css_selector("a.job-card-search__link-wrapper.js-focusable-card.ember-view")
            for e in visible_link_elements:
                try:
                    if e.get_attribute("href") not in self.all_links:
                        print(e.get_attribute("href"))
                        all_links.append(e.get_attribute("href"))
                except:
                    print("could not get the link")
            
            self.driver.execute_script("arguments[0].scrollIntoView();", visible_link_elements[-1] )
    
    def validate_link(self, link):
        
        main = self.driver.current_window_handle
        link.send_keys(Keys.CONTROL + Keys.RETURN)
        time.sleep(1.0)
        link.send_keys(Keys.CONTROL + Keys.TAB)
        self.driver.switch_to_window(main)

        time.sleep(1.0)
        #self.driver.get(link)
        time.sleep(1.0)
        self.driver.find_element_by_css_selector("button.view-more-icon").click()
        time.sleep(0.2)
        job_description = self.driver.find_element_by_css_selector("div.jobs-description__content.jobs-description-content").get_attribute("innerHTML")
        print( job_description )
        self.driver.execute_script('''window.close();''')
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
        self.driver.close()
        
    def navigate_search_results(self):
        """
        scrape postings for all pages in search results
        """
        search_results_exhausted = False
        results_page = self.results_page
        delay = 2
        time.sleep(1.0)
        
        self.all_links = []
        
        print_num_search_results(self.driver, self.data["position"], self.data["location"])
        go_to_specific_results_page(self.driver, delay, results_page)
        results_page = results_page if results_page > 1 else 1
        
        #links = driver.find_elements_by_xpath('//a[contains(@class, "job-card-search__link-wrapper js-focusable-card ember-view")]')
        while not search_results_exhausted:
            time.sleep(0.5)
            links = self.driver.find_elements_by_css_selector("a.job-card-search__link-wrapper.js-focusable-card.ember-view")
            print(len(links))
            #print("===== page",self.results_page," job links:",len(links))
            for l in links:
                try:
                    if l.get_attribute("href") in self.all_links:
                        pass
                    else:
                        elem = l.get_attribute("href")
                        self.validate_link(l)
                        print(elem)
                        self.all_links.append(elem)
                except:
                    print("["+str(datetime.datetime.now())+"] Could not get the link")
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].scrollIntoView();", links[-1] )
            time.sleep(0.5)
            links = self.driver.find_elements_by_css_selector("a.job-card-search__link-wrapper.js-focusable-card.ember-view")
            #print("===== page",self.results_page," job links:",len(links))
            for l in links:
                try:
                    if l.get_attribute("href") in self.all_links:
                        pass
                    else:
                        elem = l.get_attribute("href")
                        print(elem)
                        self.all_links.append(elem)
                except:
                    print("["+str(datetime.datetime.now())+"] Could not get the link")
                        
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # attempt to navigate to the next page of search results
            # if the link is not present, then the search results have been 
            # exhausted
            results_page += 1
            search_results_exhausted = next_results_page(self.driver, delay)
                #print("\n**************************************************")
                #print("\nNavigating to results page  {}\n".format(results_page))
                #print("\n**************************************************")
                #print("\nSearch results exhausted\n")
    def save_results(self):
        print("["+str(datetime.datetime.now())+"] Zapisuje linki do pliku....\n")
        
        f = open(self.data["location"]+"-"+self.data["content-search"]+".txt", 'w')
        for l in self.all_links:
            f.write(l+'\n')  # python will convert \n to os.linesep
        f.close()