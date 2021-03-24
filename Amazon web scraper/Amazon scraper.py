from bs4 import BeautifulSoup
import requests
import csv
import smtplib


# Extracts the title and returns it as a string
def get_title(soup):

    global title

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        # Gets the string value inside the specified tag
        # Removes leading and trailing spaces
        title = title.string.strip()

    except:
        title = ''

    return title


# Extracts the price of the product
def get_price(soup):

    global price

    try:
        price = soup.find('span', attrs = {'id' : 'priceblock_ourprice'})
        price = price.string.strip()

    except:
        price = ''

    return price


# Extracts rating of the product
def get_rating(soup):

    global rating

    try:
        rating = soup.find('span', attrs = {'class' : 'a-icon-alt'})
        rating = rating.string.strip()

    except:
        rating = ''

    return rating


# Extracts number of review counts of the product
def get_review_count(soup):

    global review_count

    try:
        review_count = soup.find('span', attrs = {'id' : 'acrCustomerReviewText'})
        review_count = review_count.string.strip()

    except:
        review_count  = ''

    return review_count


# Extracts the availablity of the product ('In Stock.' or '')
def get_availability(soup):

    global availability

    try:
        availability = soup.find('span', attrs = {'class' : 'a-size-medium a-color-success'})        
        availability = availability.string.strip()
        availability = availability[0:-1]

    except:
        availability = ''

    return availability


# Exctracts the amount of sale on the product
def get_save(soup):

    global save

    try:
        save = soup.find('td', attrs = {'class' : 'a-span12 a-color-price a-size-base priceBlockSavingsString'})  
        save = save.string.strip()

    except:
        save = ''

    return save


# Emails the link for the item with the greatest discound to the user
def email(best_product):

    sender_email = input('Enter your email address: ').strip()
    password = input('Enter your password: ').strip() 
    rec_email = input('Enter the receivers email: ').strip() 

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:   
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sender_email, password)    

        subject = 'The item with the greatest discount.'
        body = 'Link: https://www.amazon.ca' + best_product[0]

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(sender_email, rec_email, msg)

# Runs only if the file is executed as the main program
if __name__ == '__main__':

    # Initializes a list, which is later used to keep track of the product with the greatest save
    best_product = [None, 0]

    # Opens/creates csv file
    csv_file = open('amazon_scrape.csv', 'w')

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'Price', 'Rating', 'Review count', 'Availability', 'Save'])

    # User agent, tells the website about the type of host sending requests and prevents from the website blocking access
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US'})

    URL = input('Enter an Amazon search link: ').strip()
    print()
    page = requests.get(URL, headers = HEADERS)

    soup = BeautifulSoup(page.content, 'lxml')


    # Fetch all tags that have a link
    links = soup.find_all('a', attrs = {'class':'a-link-normal s-no-outline'})

    # Gets the href links in each tag
    links_list = []

    for link in links:
        links_list.append(link.get('href'))

    # Extracts the data for all products on the page
    for link in links_list: 

        new_page = requests.get('https://www.amazon.ca' + link, headers = HEADERS)
        new_soup = BeautifulSoup(new_page.content, 'lxml')

        print('Product title:', get_title(new_soup))
        print('Product price:', get_price(new_soup))
        print('Product rating:', get_rating(new_soup))
        print('Product review count:', get_review_count(new_soup))
        print('Product availability:', get_availability(new_soup))
        print('Product save:', get_save(new_soup))
        print()
        print()
        
        csv_writer.writerow([title, price, rating, review_count, availability, save])       

        # Updates the product with the highest save
        if save != '':
            save = save.split()
            save = float(save[1])

            if save > best_product[1]:
                best_product[0] = link
                best_product[1] = save

    csv_file.close()

    if None in best_product:
        exit()
    else:
        email(best_product)
        exit()
