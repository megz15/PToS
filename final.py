'''
    Program: PToS - Price Tool for Online Stores
    Version: 1.0
    Author : Meghraj Goswami
    Github : github.com/megz15/PToS
'''


###===IMPORTS===###
from random import sample,randint
from msedge.selenium_tools import Edge,EdgeOptions
from bs4 import BeautifulSoup as bs
import requests as r
from PIL import Image
from io import BytesIO
import sys,os
from threading import Thread
from webbrowser import open as wb
import PySimpleGUI as sg

###===SPLASH_SCREEN===###
def splash():
    load_anim = b'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'
    sg.theme('black')
    sg.popup_non_blocking('Loading',auto_close=True,auto_close_duration=3.5,no_titlebar=True,grab_anywhere=True,keep_on_top=True,button_type=sg.PySimpleGUI.POPUP_BUTTONS_NO_BUTTONS,font='Any 20',image=load_anim)
    #w_splash = sg.Window('',[[sg.T('Loading')]],grab_anywhere=True,keep_on_top=True,no_titlebar=True)
    #for i in range(100):
    #    e_spl,v_spl = w_splash.read(0)
splash()

###===Auto-Py-To-EXE_func===###
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


###===Set up selenium webdriver===###
options = EdgeOptions()
options.use_chromium = True     #Uses chromium-based edgium, remove to use legacy edge
options.headless = True         #Headless mode
driver = Edge(resource_path("msedgedriver.exe"),options=options)


#Enclose whole program in function to make theme dynamically changeable
def create_main_window(thm_txt,loc,looknfeel,def_search,def_sort,def_stores):

    
    ###===VARS===###
    dict_info = {}                  #Results dictionary
    inr_in_1_usd = 73.8             #Conversion for eBay and AliExpress
    rate_limit = 3.5                #Rating limit
    price_limit = 20000.0           #Highest price
    remove_lower_than_rate = False  #Remove results with rating lower than rate_limit
    remove_higher_than_price = False#Remove results with price higher than price_limit
    remove_no_free_ship = False     #Remove results that don't have free shipping
    is_rick_rolling = True          #Hehe

    
    ###===FUNCTIONS===###

    def get_img_data(f):            #Show image in PySimpleGUI from URL
        bio = BytesIO()             #BytesIO object - data stored as bytes in memory
        try:
            a = r.get(f)
        except r.exceptions.MissingSchema:
            a = r.get('https://1080motion.com/wp-content/uploads/2018/06/NoImageFound.jpg.png')
        
        img = Image.open(BytesIO(a.content))                                    #Open Image data as bytes
        img.thumbnail((220,220))                                                #,Image.ANTIALIAS - better quality, slower
        bg = Image.new('RGBA',(220,220),(255,255,255,0))                        #220x220 Image Background
        bg.paste(img,(int((220-img.size[0]) / 2), int((220-img.size[1]) / 2)))  #Resize and fit image in bg in the center
        bg.save(bio,'PNG')          #Save image as PNG
        del img                     #Delete image to reduce memory usage
        return bio.getvalue()       #Return image data in bytes

    
    ##MAIN SEARCH LOGIC##
    def search(shops:list,arrange:str,page:int):
        if values['_SEARCH_TERM_']=='':
            w['_UPDATE_'].update(' '*40+'Please enter a search term')
            w['_PAGE_'].update('00')
            return
        if not bool(shops):
            w['_UPDATE_'].update(' '*40+'Please select a store')
            w['_PAGE_'].update('00')
            return
        else:
            if looknfeel=='black':
                w['_IMG_'].update(data=get_img_data('https://megz.has-no-bra.in/OdPABq.png'))
            else:
                w['_IMG_'].update(data=get_img_data('https://megz.has-no-bra.in/Sjuvhx.png'))

        w['Search'].update(disabled=True)
        w['_BACK_'].update(disabled=True)
        w['_NEXT_'].update(disabled=True)
        w['Clear All'].update(disabled=True)
        w.set_cursor('watch')
        w['_RESULTS_'].update([])   #Clear results listbox
        dict_info.clear()           #Clear results dictionary

        if 'amazon' in shops:       #Index Amazon
            w['_UPDATE_'].update(' '*45+'Indexing Amazon.in...')
            if arrange=='Featured':
                am_url = 'https://www.amazon.in/s?k='+values['_SEARCH_TERM_'].replace(' ','+')+'&page='+str(page)
            
            elif arrange=='Low to High':
                am_url = 'https://www.amazon.in/s?k='+values['_SEARCH_TERM_'].replace(' ','+')+'&s=price-asc-rank&page='+str(page)
            
            elif arrange=='High to Low':
                am_url = 'https://www.amazon.in/s?k='+values['_SEARCH_TERM_'].replace(' ','+')+'&s=price-desc-rank&page='+str(page)
            
            driver.get(am_url)
            html_amazon = driver.page_source                #HTML source code
            soup_amazon = bs(html_amazon,'html.parser')     #Create soup object
            
            for i in soup_amazon.find_all('div',{'data-component-type':'s-search-result'}):         #Search results
                
                titles_am  = i.find('span',{'class':'a-size-medium a-color-base a-text-normal'})    #Title
                if titles_am == None:
                    titles_am = i.find('span',{'class':'a-size-base-plus a-color-base a-text-normal'})
                title_am = titles_am.get_text()
                
                rates_am = i.find('span',{'class':'a-icon-alt'})    #Rating
                if rates_am == None:
                    rate_am = 'Nil'
                    if remove_lower_than_rate:
                        continue
                else:
                    rate_am = rates_am.get_text()
                    if remove_lower_than_rate:
                        if float(rate_am.split()[0])<rate_limit:
                            continue
                
                review_container = i.find('div',{'class':'a-row a-size-small'})     #Reviews
                try:
                    reviews_am = review_container.find('span',{'class':'a-size-base'})
                except:
                    reviews_am = None
                if reviews_am == None:
                    review_am = 'Nil'
                else:
                    review_am = reviews_am.get_text()

                price_n_am = i.find('span',{'class':'a-price-whole'})   #Price
                if price_n_am == None:
                    price_new_am = 'Nil'
                    if remove_higher_than_price:
                        continue
                else:
                    price_new_am = price_n_am.get_text()
                    if remove_higher_than_price:
                        if float(price_new_am.replace(',',''))>price_limit:
                            continue

                get_bys_am = i.find('span',{'class':'a-text-bold'})     #Delivery date
                if get_bys_am == None:
                    get_by_am = 'Nil'
                else:
                    get_by_am = get_bys_am.get_text()

                deals_am = i.find('span',{'class':'a-color-price'})     #Special deals
                if deals_am == None:
                    deal_am = 'Nil'
                else:
                    deal_am = deals_am.get_text()

                img_am = i.find('img',{'class':'s-image','data-image-latency':'s-product-image'})['src']   #Product Image

                product_am = 'https://amazon.in'+i.find('a',{'class':'a-link-normal s-no-outline'})['href']

                dict_info[title_am[:40]+'...'] = (title_am,rate_am,review_am,price_new_am,get_by_am,deal_am,product_am,img_am,'am') #Store result

        if 'flipkart' in shops:     #Index Flipkart
            w['_UPDATE_'].update(' '*45+'Indexing Flipkart.com...')
            if arrange=='Featured':
                fk_url = 'https://www.flipkart.com/search?q='+values['_SEARCH_TERM_'].replace(' ','+')+'&page='+str(page)
            
            elif arrange=='Low to High':
                fk_url = 'https://www.flipkart.com/search?q='+values['_SEARCH_TERM_'].replace(' ','+')+'&sort=price_asc&page='+str(page)
            
            elif arrange=='High to Low':
                fk_url = 'https://www.flipkart.com/search?q='+values['_SEARCH_TERM_'].replace(' ','+')+'&sort=price_desc&page='+str(page)
            
            driver.get(fk_url)
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            m = 0
            for i in range(50):
                driver.execute_script('scroll('+str(m)+', '+str(m+250)+')')
                m+=250
            html_flipkart = driver.page_source
            soup_flipkart = bs(html_flipkart,'html.parser')

            #small box results
            for j in soup_flipkart.find_all('div',{'class':'_4ddWXP'}):
            
                titles_fk = j.find('a',{'class':'s1Q9rs'})
                title_fk = titles_fk.get_text()

                rates_fk = j.find('div',{'class':'_3LWZlK'})
                if rates_fk == None:
                    rate_fk = 'Nil'
                    if remove_lower_than_rate:
                        continue
                else:
                    rate_fk = rates_fk.get_text()
                    if remove_lower_than_rate:
                        if float(rate_fk)<rate_limit:
                            continue

                reviews_fk = j.find('span',{'class':'_2_R_DZ'})
                if reviews_fk == None:
                    review_fk = 'Nil'
                else:
                    review_fk = reviews_fk.get_text()

                price_n_fk = j.find('div',{'class':'_30jeq3'})
                if price_n_fk == None:
                    price_new_fk = 'Nil'
                    if remove_higher_than_price:
                        continue
                else:
                    price_new_fk = price_n_fk.get_text().lstrip('₹')
                    if remove_higher_than_price:
                        if float(price_new_fk.replace(',',''))>price_limit:
                            continue

                #get_bys_fk = j.find('span',{'class':'a-text-bold'})
                #if get_bys_fk == None:
                #    get_by_fk = 'Nil'
                #else:
                #    get_by_fk = get_bys_fk.get_text()
                get_by_fk = 'Nil'

                deals_fk = j.find('div',{'class':'_3Ay6Sb'})
                if deals_fk == None:
                    deals_fk = j.find('div',{'class':'_2ZdXDB'})
                    if deals_fk ==None:
                        deals_fk = j.find('div',{'class':'_18hQoS'})
                try:
                    deal_fk = deals_fk.get_text()
                except AttributeError:
                    deal_fk = 'No Cost EMI'

                img_fk = j.find('img',{'class':'_396cs4'})['src']

                product_fk = 'https://www.flipkart.com'+j.find('a',{'class':'_2rpwqI'})['href']
                
                dict_info[title_fk[:40]+'...'] = (title_fk,rate_fk,review_fk,price_new_fk,get_by_fk,deal_fk,product_fk,img_fk,'fk')

            #larger results
            try:
                for j in soup_flipkart.find_all('div',{'class':'_13oc-S'}):
            
                    titles_fk = j.find('div',{'class':'_4rR01T'})
                    title_fk = titles_fk.get_text()

                    rates_fk = j.find('div',{'class':'_3LWZlK'})
                    if rates_fk == None:
                        rate_fk = 'Nil'
                        if remove_lower_than_rate:
                            continue
                    else:
                        rate_fk = rates_fk.get_text()
                        if remove_lower_than_rate:
                            if float(rate_fk)<rate_limit:
                                continue

                    reviews_fk = j.find('span',{'class':'_2_R_DZ'})
                    if reviews_fk == None:
                        review_fk = 'Nil'
                    else:
                        review_fk = reviews_fk.get_text()

                    price_n_fk = j.find('div',{'class':'_30jeq3'})
                    if price_n_fk == None:
                        price_new_fk = 'Nil'
                        if remove_higher_than_price:
                            continue
                    else:
                        price_new_fk = price_n_fk.get_text().lstrip('₹')
                        if remove_higher_than_price:
                            if float(price_new_fk.replace(',',''))>price_limit:
                                continue

                    #get_bys_fk = j.find('span',{'class':'a-text-bold'})
                    #if get_bys_fk == None:
                    #    get_by_fk = 'Nil'
                    #else:
                    #    get_by_fk = get_bys_fk.get_text()
                    get_by_fk = 'Nil'

                    deals_fk = j.find('div',{'class':'_3Ay6Sb'})
                    if deals_fk == None:
                        deals_fk = j.find('div',{'class':'_2ZdXDB'})
                        if deals_fk ==None:
                            deals_fk = j.find('div',{'class':'_18hQoS'})
                    try:
                        deal_fk = deals_fk.get_text()
                    except AttributeError:
                        deal_fk = 'No Cost EMI'

                    img_fk = j.find('img',{'class':'_396cs4'})['src']

                    product_fk = 'https://www.flipkart.com'+j.find('a',{'class':'_1fQZEK'})['href']
                    
                    dict_info[title_fk[:40]+'...'] = (title_fk,rate_fk,review_fk,price_new_fk,get_by_fk,deal_fk,product_fk,img_fk,'fk')
            
            except AttributeError:
                pass

        if 'aliexpress' in shops:   #Index AliExpress
            w['_UPDATE_'].update(' '*45+'Indexing AliExpress.com...')
            #driver.get('https://www.aliexpress.com')
            #driver.find_element_by_class_name('search-key').send_keys(values['_SEARCH_TERM_'], Keys.RETURN)
            
            if arrange=='Featured':
                ax_url = 'https://www.aliexpress.com/wholesale?SearchText='+values['_SEARCH_TERM_'].replace(' ','+')+'&page='+str(page)
            
            elif arrange=='Low to High':
                ax_url = 'https://www.aliexpress.com/wholesale?SearchText='+values['_SEARCH_TERM_'].replace(' ','+')+'&SortType=price_asc&page='+str(page)
            
            elif arrange=='High to Low':
                ax_url = 'https://www.aliexpress.com/wholesale?SearchText='+values['_SEARCH_TERM_'].replace(' ','+')+'&SortType=price_desc&page='+str(page)

            #PROXY = choice(ind).get_address()
            #webdriver.DesiredCapabilities.CHROME['proxy']={
            #    "httpProxy":PROXY,
            #    "ftpProxy":PROXY,
            #    "sslProxy":PROXY,
            #    "proxyType":"MANUAL",
            #}
            driver.get(ax_url)
            m = 0
            for i in range(100):
                driver.execute_script('scroll('+str(m)+', '+str(m+250)+')')
                m+=250
            html_ali = driver.page_source
            soup_ali = bs(html_ali,'html.parser')
            
            for k in soup_ali.find_all('div',{'class':'gallery product-card middle-place'}):
            
                titles_ax  = k.find('a',{'class':'item-title'})
                title_ax = titles_ax.get_text()
                
                rates_ax = k.find('span',{'class':'rating-value'})
                if rates_ax == None:
                    rate_ax = 'Nil'
                    if remove_higher_than_price:
                        continue
                else:
                    rate_ax = rates_ax.get_text()
                    if remove_lower_than_rate:
                        if float(rate_ax)<rate_limit:
                            continue
                
                reviews_ax = k.find('a',{'class':'sale-value-link'})
                if reviews_ax == None:
                    review_ax = 'Nil'
                else:
                    review_ax = reviews_ax.get_text()

                price_n_ax = k.find('span',{'class':'price-current'})
                if price_n_ax == None:
                    price_new_ax = 'Nil'
                    if remove_higher_than_price:
                        continue
                else:
                    try:
                        price_new_ax = str(round(float(price_n_ax.get_text()[:price_n_ax.get_text().find(' - ')].lstrip('US $'))*inr_in_1_usd,2))
                        if remove_higher_than_price:
                            if float(rate_ax)>price_limit:
                                continue
                    except:
                        price_new_ax = price_n_ax.get_text()

                ships_ax = k.find('span',{'class':'shipping-value'})
                if ships_ax == None:
                    ship_ax = 'Nil'
                    if remove_no_free_ship:
                        continue
                else:
                    try:
                        ship_ax = '₹'+str(round(float(ships_ax.get_text().lstrip('+ Shipping: US $'))*inr_in_1_usd,2))
                        if remove_no_free_ship:
                            continue
                    except:
                        ship_ax = ships_ax.get_text()
                        if remove_no_free_ship:
                            if 'free' not in ship_ax.lower():
                                continue

                stores_name_ax = k.find('a',{'class':'store-name'})
                if stores_name_ax == None:
                    store_ax = 'Nil'
                else:
                    store_ax = stores_name_ax.get_text()

                img_ax = 'https:'+k.find('img',{'class':'item-img'})['src']

                product_ax = k.find('a',{'class':'item-title'})['href'][2:]

                dict_info[title_ax[:40]+'...'] = (title_ax,rate_ax,review_ax,price_new_ax,ship_ax,store_ax,product_ax,img_ax,'ax')
        
        if 'ebay' in shops:         #Index eBay
            w['_UPDATE_'].update(' '*45+'Indexing eBay.com...')
            if arrange=='Featured':
                eb_url = 'https://www.ebay.com/sch/i.html?_nkw='+values['_SEARCH_TERM_'].replace(' ','+')+'&_pgn='+str(page)
            
            elif arrange=='Low to High':
                eb_url = 'https://www.ebay.com/sch/i.html?_nkw='+values['_SEARCH_TERM_'].replace(' ','+')+'&_sop=15&_pgn='+str(page)
            
            elif arrange=='High to Low':
                eb_url = 'https://www.ebay.com/sch/i.html?_nkw='+values['_SEARCH_TERM_'].replace(' ','+')+'&_sop=16&_pgn='+str(page)

            driver.get(eb_url)
            html_ebay = driver.page_source
            soup_ebay = bs(html_ebay,'html.parser')
            
            for l in soup_ebay.find_all('div',{'class':'s-item__wrapper clearfix'}):
            
                titles_eb  = l.find('h3',{'class':'s-item__title'})
                title_eb = titles_eb.get_text()
                
                rate_container = l.find('div',{'class':'x-star-rating'})
                try:
                    rates_eb = rate_container.find('span',{'class':'clipped'})
                except:
                    rates_eb = None
                if rates_eb == None:
                    rate_eb = 'Nil'
                    if remove_lower_than_rate:
                        continue
                else:
                    rate_eb = rates_eb.get_text()
                    if remove_lower_than_rate:
                        if float(rate_eb.split()[0])<rate_limit:
                            continue
                
                reviews_eb = l.find('span',{'class':'s-item__reviews-count'})
                if reviews_eb == None:
                    review_eb = 'Nil'
                else:
                    review_eb = reviews_eb.get_text()

                price_n_eb = l.find('span',{'class':'s-item__price'})
                if price_n_eb == None:
                    price_new_eb = 'Nil'
                    if remove_higher_than_price:
                        continue
                else:
                    try:
                        price_new_eb = str(round(float(price_n_eb.get_text()[:price_n_eb.get_text().find(' to ')].lstrip('$').replace(',',''))*inr_in_1_usd,2))
                        if remove_higher_than_price:
                            if price_new_eb>price_limit:
                                continue
                    except:
                        price_new_eb = str(round(float(price_n_eb.get_text().lstrip('$').replace(',','')),2))

                ships_eb = l.find('span',{'class':'s-item__shipping s-item__logisticsCost'})
                if ships_eb == None:
                    ship_eb = 'Nil'
                    if remove_no_free_ship:
                        continue
                else:
                    try:
                        ship_eb = '₹'+str(round(float(ships_eb.get_text().lstrip('+$').rstrip(' shipping'))*inr_in_1_usd,2))
                        if remove_no_free_ship:
                            continue
                    except:
                        ship_eb = ships_eb.get_text()
                        if remove_no_free_ship:
                            if 'free' not in ship_eb.lower():
                                continue

                country_from_eb = l.find('span',{'class':'s-item__location'})
                if country_from_eb == None:
                    store_eb = 'Nil'
                else:
                    store_eb = country_from_eb.get_text()

                img_eb = l.find('img',{'class':'s-item__image-img'})

                product_eb = l.find('a',{'class':'s-item__link'})['href']

                dict_info[title_eb[:40]+'...'] = (title_eb,rate_eb,review_eb,price_new_eb,ship_eb,store_eb,product_eb,img_eb['src'],'eb')

        w['_IMG_'].update(data=get_img_data(('https://megz.has-no-bra.in/6hOjAw.png' if looknfeel=='black' else 'https://megz.has-no-bra.in/zQYpMr.png')))
        w['Search'].update(disabled=False)
        if page!=1:
            w['_BACK_'].update(disabled=False)
        w['_NEXT_'].update(disabled=False)
        w['Clear All'].update(disabled=False)
        w.set_cursor('arrow')
        if bool(dict_info):         #If results found

            w['_UPDATE_'].update(' '*23+'Crawled through all stores and found '+str(len(list(dict_info.keys())))+' results!')
            
            if sort_type=='Low to High':
                dict_low = {z:dict_info[z] for z in dict_info if dict_info[z][3]!='Nil'}
                w['_RESULTS_'].update(sorted(dict_low,key=lambda x: float(dict_low[x][3].replace(',',''))))
            
            elif sort_type=='High to Low':
                dict_high = {z:dict_info[z] for z in dict_info if dict_info[z][3]!='Nil'}
                w['_RESULTS_'].update(sorted(dict_high,key=lambda x: float(dict_high[x][3].replace(',','')),reverse=True))
            
            elif sort_type=='Featured':
                w['_RESULTS_'].update(sample(list(dict_info.keys()),len(dict_info)))
            
            w['_PAGE_'].update(str(page).zfill(2))
        
        else:                       #If results not found
            w['_UPDATE_'].update(' '*35+'Error while searching, try again')
            w['_PAGE_'].update('00')

            def popup_error():      #Error popup
                sg.theme(('darkbrown5' if looknfeel=='black' else 'darkbrown6'))
                l_err  = [[sg.Image(resource_path('error.gif'),key='_ERRIMG_',background_color='black')],
                          [sg.T('Search failed! Try again?')],
                          [sg.B('Aye!',size=(5,None),button_color=('black',('lawngreen' if looknfeel=='black' else 'darkgreen'))),sg.B('Nay',size=(5,None),button_color=('black',('tomato' if looknfeel=='black' else 'red3')))]]
                w_err = sg.Window('',l_err,grab_anywhere=True,keep_on_top=True,margins=(5,5),no_titlebar=True,element_justification='center',alpha_channel=0.95)
                while True:
                    e_er,v_er = w_err.read(0)
                    w_err['_ERRIMG_'].update_animation(resource_path('error.gif'),time_between_frames=50)
                    if e_er=='Aye!':
                        w_err.Close()
                        Thread(target=search,args=(stores,sort_type,1)).start()
                        break
                    elif e_er=='Nay':
                        w_err.Close()
                        break
                #if sg.popup_yes_no('Search failed. Try again?',title='!')=='Yes':
                #    Thread(target=search,args=(stores,sort_type,page)).start()
                #else:
                #    pass
            Thread(target=popup_error,daemon=True).start()
            #if sg.popup_yes_no('Search failed. Try again?',title='!')=='Yes':
            #    Thread(target=search,args=(stores,sort_type,page)).start()
            #else:
            #    pass

    def change_page(dir):           #Change page
        try:
            page = int(driver.current_url[-1])
        except ValueError:
            page = 1
        
        if dir=='next':
            Thread(target=search,args=(stores,sort_type,page+1)).start()
        
        if dir=='back':
            Thread(target=search,args=(stores,sort_type,page-1)).start()

    sg.theme(looknfeel)             #Main window theme

    col_info = [[sg.T('Product Name and Reviews',key='_TITLE_',size=(25,None),text_color=('orange' if looknfeel=='black' else 'darkorange4'))],    #Product info column
                [sg.T('Product Price',key='_PRICE_',size=(12,None)),sg.T('Special Product Deals',text_color=('hotpink' if looknfeel=='black' else 'purple'),key='_DEALS_',size=(12,None))],
                [sg.T('Shipping Price / Delivery date',key='_DATE_',size=(12,None),text_color=('cyan' if looknfeel=='black' else 'navy')),sg.T('Product Rating',key='_RATE_',size=(12,None))]]

    col_shop_options = [[sg.Check('Amazon',default=(True if 0 in def_stores else False))],  #Online stores available to search
                        [sg.Check('Flipkart',default=(True if 1 in def_stores else False))],
                        [sg.Check('Aliexpress',default=(True if 2 in def_stores else False))],
                        [sg.Check('eBay',default=(True if 3 in def_stores else False))]]

    col_shop_open_stores = [[sg.B('  ',font='Courier 7',key='_OPNAM_',pad=(None,6),tooltip='\n   Open Amazon.in   \n')],
                            [sg.B('  ',font='Courier 7',key='_OPNFK_',pad=(None,6),tooltip='\n   Open Flipkart.com   \n')],
                            [sg.B('  ',font='Courier 7',key='_OPNAX_',pad=(None,6),tooltip='\n   Open AliExpress.com   \n')],
                            [sg.B('  ',font='Courier 7',key='_OPNEB_',pad=(None,6),tooltip='\n   Open eBay.com   \n')]]

    frame_shops = [[sg.Col(col_shop_options),sg.Col(col_shop_open_stores)]]

    col_config = [[sg.T('--Options--',pad=(10,(5,5)))],        #Options column
                [sg.Frame('Stores',frame_shops,pad=(10,(5,20)),)],
                [sg.Combo(['Low to High','Featured','High to Low'],default_value=def_sort,key='_ARRANGE_',size=(15,None),pad=(10,(5,15)),readonly=True)],
                [sg.B('Advanced Settings',key='_MORE_',size=(15,None),pad=(10,(5,15)))]]

    #Image Frame
    frame_img = [[sg.Image(data=get_img_data(('https://megz.has-no-bra.in/6hOjAw.png' if looknfeel=='black' else 'https://megz.has-no-bra.in/zQYpMr.png')),key='_IMG_',size=(200,200),enable_events=True)]]

    col_results = [[sg.Listbox([],enable_events=True,key='_RESULTS_',size=(40,12))],    #Results column
                [sg.T(' ',font='Courier 9')],
                [sg.B(' < Back ',key='_BACK_',tooltip=' Go to the page before ',disabled=True),sg.T('00',key='_PAGE_',size=(2,1),tooltip=' Page number '),sg.B(' Next > ',key='_NEXT_',tooltip=' Go to the next page ',disabled=True)]]

    icon_dark = b'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'
    icon_lite = b'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'
    icon_gift = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAEb0lEQVRoge2YXUxbZRzGf+ecfkE/6RQZjkkcOC6MUTMSI+NiV9uS4ZVImMbgRxbvt2W7WDLmlUvwXq+8EYgbWzamUZewGYGYLE4vzL7IMIwygZS2rHQdpe15vSjQ0vaUnXPKMIYnafKe//v/eJ6834UtbGHzMNlPR6CP+cl+TumJmxviVOga86HrdJjlIBkNnOqlXUj0AZblTGfrOjm5XlxoiG4kTi9/piWJLv8+vjXKQzYSNNlPxxryAIITgV66S8XlkQdQhOAbMyNhSIAk+Jpc8qsdnNYSUYT8CiwIvjLCAwwKEBI9mp1FRJQgn8kn+NIIj0w5gwj0cgKJL0pkPlvXycn1yCPRvW0fZ4zyMCwA1hdh8zJqqaClRHVT5DMpTEJLhNWV+ZWobJp8Jk0O5j47OioEbxtNJncUTmX1u6NG0xEeu6/RI0Z2Xx9shbxFbIb8s4W0d6VlaBf6L2FLwGYjX8DIprDQC8HwSrPoNvrn9iZhJO/O3rsFtsn3m3TnmUolNfvaguNrOP/vppBhaA2ZoaHUAdMCUgjiVQmUQ8Gi/cqhII+rEqQ2SErhlVgHFpQU/vfmqD/wCNlSnOCOzhDqu2FmfvISOf8c7rSpkgUwlE0AMdcSO48/xN2QWNdftgpq2+ZxNT0h0PMi7pjNSNniuY0ERZUUdceejnwuPI0J6o79Q1ROGSlbFLoFxIWKvz2Ip1Ef+RV4Ghfxtc8RF6qh+HzomkICSFYtsf1gNGu88RqMNMOCE+qnYP8w1ARhuhqu7oWJHeB+DK03oPkvAGoPPuLWzz7EvMP0fV6XgIRQcbdGswv25qtwcX/W4c4uuP8StPwOo3sguZz+iR0uHABFhTdvIVsF7pYoie9tOCRzG6Gu6EUh8L0ezxqG9xQ6JS3wy1tZ8rn4tXm16X0jzqIwv7XqEpBCUFGTc8xHvPqq5fhX1iTLcjboEpAWYHXlLL5dk/qqNTxYbVrcKukynG26J2ByISfknSFwxbWdc+GMQ9u1bJ5oeW4xurIoEsRnrVmDLwqfnoOKxdKBjgR8MpDxX0Z81opi+i8FnQIsSIT+qFhrrAnCxwNgXyoeZEtC10WonV1jDt2sxGL+TxF9AhySRHjUjZrMK1w3DR8NZMjmwpqCrguZ8yEHalIi8psLh/SMBdglGSVk48GPnsLO+ofw4SWwpDPfSho+uAwvBwpcJ37woIRs2E2eAaBTgAQ4ZZnpc34iY/ZCh4YJ6LwC3gU4fAV2/13gEhmzM3vej1OWyzCBDD4p59U0MdcSTcdn8L/y9Hei8D0793pqcMZs+GRF02/Dn5Q+WcEZs3H7TC3jlz2FayIPalJi/JKH25/XUrkOeb0w/LqokhUUFYL9zzNz1cu2lhhNhyMFfnf7qpgbcWEJ2/BJMp4ykgeTT0qPrFCtWHCHHUQH/UV9ooN+PBEH1Yql7OTB5JMyk0DCJysIipN7QbGWZbFqQWsEpjTsmtAiWWbyBXtyUQFCqEcwIGKDEZDhyGaT2MIWtlBm/AsgemBUtoE5UgAAAABJRU5ErkJggg=='
    
    #Main window layout
    layout = [[sg.T(' '*25),sg.I(def_search,size=(25,None),key='_SEARCH_TERM_',tooltip=' Enter search term '),sg.B('Search'),sg.T(key='_INDEX_'),sg.T(' '*7),sg.B(image_data=(icon_lite if looknfeel=='black' else icon_dark),button_color=(sg.theme_background_color(),sg.theme_background_color()),key='_THEME_',border_width=0,image_subsample=2,tooltip='\n   Change theme   \n')],
              [sg.T(thm_txt,key='_UPDATE_',size=(50,None),text_color=('gray' if looknfeel=='black' else 'black'))],
              [sg.Col(col_config,element_justification='center',key='COL1'),sg.Col(col_results,element_justification='center')],
              [sg.Frame('',frame_img),sg.Col(col_info,element_justification='center',)],
              [sg.T()],
              [sg.B(image_data=icon_gift,button_color=(sg.theme_background_color(),sg.theme_background_color()),key='_GIFT_',tooltip='\n  Hehe  \n',border_width=0),sg.T(' '*40 ),sg.B('Clear All',size=(8,None),tooltip='\n  Clear all fields  \n'),sg.B('About',size=(8,None),tooltip='\n  About the program  \n'),sg.B('Exit',size=(8,None),tooltip='\n  Exit the program  \n')]]

    icon_window = b'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'
    w=sg.Window('Price Tool for Online Stores - PToS',layout,button_color=('black','royalblue1'),icon=icon_window,location=loc,finalize=True)     #Create main window

    ###===Set Cursors===###
    w['_IMG_'].set_cursor('hand2')
    w['About'].set_cursor('question_arrow')
    w['Exit'].set_cursor('no')
    w['_MORE_'].set_cursor('plus')
    w['_THEME_'].set_cursor('spraycan')
    w['_GIFT_'].set_cursor('gumby')
    w['_BACK_'].set_cursor('sb_left_arrow')
    w['_NEXT_'].set_cursor('sb_right_arrow')

    while True:                     #Main window loop    
        event,values = w.read()     #Get main window events and values
        
        if event in (sg.WIN_CLOSED,'Exit'):    #Close main window
            break

        if event=='Search':         #'Search' event generated by pressing 'Search' button
            stores = []             #Store selected stores
            
            if values[0]:
                stores.append('amazon')
            
            if values[1]:
                stores.append('flipkart')
            
            if values[2]:
                stores.append('aliexpress')
            
            if values[3]:
                stores.append('ebay')
            
            sort_type = values['_ARRANGE_']                             #Get sorting type
            
            Thread(target=search,args=(stores,sort_type,1)).start()     #Call Search function
        
        if event=='_MORE_':         #Advanced options
            sg.theme('darktanblue')       #Advanced options window theme
            
            layout_options = [[sg.T('Enter preferred rating value:'),sg.In(rate_limit,size=(10,None),key='_RLT_')], #Advanced options layout
                            [sg.T('Remove results lower than this rating'),sg.Check('',default=remove_lower_than_rate)],
                            [sg.T()],
                            [sg.T('Enter preferred price value :'),sg.In(price_limit,size=(10,None),key='_PLT_')],
                            [sg.T('Remove results higher than this price'),sg.Check('',default=remove_higher_than_price)],
                            [sg.T()],
                            [sg.T('Just show products with free shipping'),sg.Check('',default=remove_no_free_ship)],
                            [sg.T()],
                            [sg.B('Set Values')]]
            
            window_options = sg.Window('Advanced options',layout_options)   #Create advanced options window
            
            while True:             #Advanced options window loop
                event_op, values_op = window_options.read() #Get advanced options window events and values
                
                if event_op==sg.WIN_CLOSED: #Close advanced options window
                    break
                
                if event_op=='Set Values':
                    if values_op[0]:        #Remove results with rating lower than rate_limit
                        remove_lower_than_rate = True
                    else:
                        remove_lower_than_rate = False
                    
                    if values_op[1]:        #Remove results with price higher than price_limit
                        remove_higher_than_price = True
                    else:
                        remove_higher_than_price = False
                    
                    if values_op[2]:        #Remove results without free shipping
                        remove_no_free_ship = True
                    else:
                        remove_no_free_ship = False
                    
                    try:
                        rate_limit = float(values_op['_RLT_'])
                        price_limit = float(values_op['_PLT_'])
                        window_options.Close()
                        #sg.PopupTimed('Values set!',auto_close_duration=5)
                    except:
                        sg.PopupError('Values can only be string!',title='Error')
        
        if event=='_RESULTS_':
            try:
                rate_txt_end = '/5'
                deal_txt = 'Deals: '
                ship_txt = 'Shipping: '
                
                #Different ways of displaying information for different stores
                if dict_info[values['_RESULTS_'][0]][-1] == 'am':
                    w['_UPDATE_'].update(' '*30+'Selected a product from Amazon.in')
                    rate_txt_end = ''
                    product_origin = 'Amazon: '
                    ship_txt = 'Get it by '
                
                elif dict_info[values['_RESULTS_'][0]][-1] == 'fk':
                    w['_UPDATE_'].update(' '*30+'Selected a product from Flipkart.com')
                    product_origin = 'Flipkart: '
                    ship_txt = 'Nil: '
                
                elif dict_info[values['_RESULTS_'][0]][-1] == 'ax':
                    w['_UPDATE_'].update(' '*30+'Selected a product from AliExpress.com')
                    product_origin = 'Aliexpress: '
                    deal_txt = 'Store: '
                
                elif dict_info[values['_RESULTS_'][0]][-1] == 'eb':
                    w['_UPDATE_'].update(' '*30+'Selected a product from eBay.com')
                    product_origin = 'eBay: '
                    deal_txt = 'Country: '
                    rate_txt_end = ''
                
                try:    #Price_limit colours (red - higher / green - equal or lower)
                    if float(dict_info[values['_RESULTS_'][0]][3].replace(',',''))<=price_limit:
                        if looknfeel=='black':
                            f_t_col = 'lawngreen'
                        else:
                            f_t_col = 'darkgreen'
                    else:
                        if looknfeel=='black':
                            f_t_col = 'tomato'
                        else:
                            f_t_col = 'red3'
                except ValueError:
                    if looknfeel=='black':
                            f_t_col = 'tomato'
                    else:
                        f_t_col = 'red3'

                try:    #Rate_limit colours (red - lower / green - equal or higher)
                    if float(dict_info[values['_RESULTS_'][0]][1].split()[0])<rate_limit:
                        if looknfeel=='black':
                            r_t_col = 'tomato'
                        else:
                            r_t_col = 'red3'
                    else:
                        if looknfeel=='black':
                            r_t_col = 'lawngreen'
                        else:
                            r_t_col = 'darkgreen'
                except ValueError:
                    if looknfeel=='black':
                            r_t_col = 'tomato'
                    else:
                        r_t_col = 'red3'

                #Update product info column with relevant product information
                w['_IMG_'].update(data=get_img_data(dict_info[values['_RESULTS_'][0]][-2].rstrip('?q=70')))
                w['_TITLE_'].update(product_origin+dict_info[values['_RESULTS_'][0]][0]+'  ('+dict_info[values['_RESULTS_'][0]][2]+')')
                w['_PRICE_'].update(text_color=f_t_col)
                w['_PRICE_'].update('Price: ₹'+dict_info[values['_RESULTS_'][0]][3])
                w['_DEALS_'].update(deal_txt+dict_info[values['_RESULTS_'][0]][5])
                w['_DATE_'].update(ship_txt+dict_info[values['_RESULTS_'][0]][4])
                w['_RATE_'].update(text_color=r_t_col)
                w['_RATE_'].update('Rating: '+dict_info[values['_RESULTS_'][0]][1]+rate_txt_end)
            
            except IndexError:
                pass

        if event=='_IMG_':      #Click on image to go to product page
            try:
                wb(dict_info[values['_RESULTS_'][0]][-3])
            except IndexError:
                pass
        
        if event=='_BACK_':     #Go the the page before
            change_page('back')
        
        if event=='_NEXT_':     #Go to the next page
            change_page('next')

        if event=='_OPNAM_':    #Open Amazon.in
            sort_type = values['_ARRANGE_']
            if sort_type=='Featured':
                url = 'https://www.amazon.in/s?k='+values['_SEARCH_TERM_'].replace(' ','+')
            
            elif sort_type=='Low to High':
                url = 'https://www.amazon.in/s?k='+values['_SEARCH_TERM_'].replace(' ','+')+'&s=price-asc-rank'
            
            elif sort_type=='High to Low':
                url = 'https://www.amazon.in/s?k='+values['_SEARCH_TERM_'].replace(' ','+')+'&s=price-desc-rank'
            wb(url)

        if event=='_OPNFK_':    #Open Flipkart.com
            sort_type = values['_ARRANGE_']
            if sort_type=='Featured':
                url = 'https://www.flipkart.com/search?q='+values['_SEARCH_TERM_'].replace(' ','+')
            
            elif sort_type=='Low to High':
                url = 'https://www.flipkart.com/search?q='+values['_SEARCH_TERM_'].replace(' ','+')+'&sort=price_asc'
            
            elif sort_type=='High to Low':
                url = 'https://www.flipkart.com/search?q='+values['_SEARCH_TERM_'].replace(' ','+')+'&sort=price_desc'
            wb(url)

        if event=='_OPNAX_':    #Open AliExpress.com
            sort_type = values['_ARRANGE_']
            if sort_type=='Featured':
                url = 'https://www.aliexpress.com/wholesale?SearchText='+values['_SEARCH_TERM_'].replace(' ','+')
            
            elif sort_type=='Low to High':
                url = 'https://www.aliexpress.com/wholesale?SearchText='+values['_SEARCH_TERM_'].replace(' ','+')+'&SortType=price_asc'
            
            elif sort_type=='High to Low':
                url = 'https://www.aliexpress.com/wholesale?SearchText='+values['_SEARCH_TERM_'].replace(' ','+')+'&SortType=price_desc'
            wb(url)

        if event=='_OPNEB_':    #Open eBay.com
            sort_type = values['_ARRANGE_']
            if sort_type=='Featured':
                url = 'https://www.ebay.com/sch/i.html?_nkw='+values['_SEARCH_TERM_'].replace(' ','+')
            
            elif sort_type=='Low to High':
                url = 'https://www.ebay.com/sch/i.html?_nkw='+values['_SEARCH_TERM_'].replace(' ','+')+'&_sop=15'
            
            elif sort_type=='High to Low':
                url = 'https://www.ebay.com/sch/i.html?_nkw='+values['_SEARCH_TERM_'].replace(' ','+')+'&_sop=16'
            wb(url)

        if event=='About':
            sg.theme('darktanblue')
            sg.Popup('Price Tool for Online Stores - PToS\nVersion: 1.0\n\nMade with 🖤 by Meghraj Goswami\n\n© 2020. All Rights Reserved',title='About PToS',font=('Any 15'))
        
        if event=='_THEME_':    #Change theme dynamically
            loc_before = w.CurrentLocation()
            search_term = values['_SEARCH_TERM_']
            arrangement = values['_ARRANGE_']
            stores_list = []
            if values[0]:
                stores_list.append(0)
            if values[1]:
                stores_list.append(1)
            if values[2]:
                stores_list.append(2)
            if values[3]:
                stores_list.append(3)
            
            default_rate = rate_limit
            default_price = price_limit
            rrate = remove_lower_than_rate
            rprice = remove_higher_than_price
            rship = remove_no_free_ship

            if looknfeel == 'black':
                w.close()
                a = ' '*25+'Theme changed to Light Mode! ٩(◕‿◕｡)۶*:･ﾟ✧'
                create_main_window(a,loc_before,'lightgreen1',search_term,arrangement,stores_list)
            else:
                w.close()
                a = ' '*28+'Theme changed to Dark Mode! (｡▼皿▼)'
                create_main_window(a,loc_before,'black',search_term,arrangement,stores_list)

        if event=='Clear All':  #Reset all fields
            dict_info.clear()
            w['_UPDATE_'].update(' '*50+'Cleared all fields')
            w['_SEARCH_TERM_'].update('')
            w['_ARRANGE_'].update('Featured')
            w[0].update(True)
            w[1].update(False)
            w[2].update(False)
            w[3].update(False)
            w['_PAGE_'].update('00')
            w['_RESULTS_'].update([])
            rate_limit,price_limit = 3.5,20000.0
            remove_higher_than_price = False
            remove_lower_than_rate = False
            remove_no_free_ship = False

        if event=='_GIFT_':
            ###===R===###
            def rick_roll():
                w_rick = sg.Window('',[[sg.Image(resource_path('rick.gif'),key='_ROLL_',enable_events=True,right_click_menu=['','Exit'],pad=(0,0))]],grab_anywhere=True,keep_on_top=True,margins=(0,0),no_titlebar=True,location=(randint(0,1300),randint(0,600)),alpha_channel=0.9)
                while True:
                    e_r,v_r = w_rick.read(0)
                    if e_r=='Exit':
                        w_rick.close()
                        break
                    if e_r=='_ROLL_':
                        Thread(target=rick_roll,daemon=True).start()
                    w_rick['_ROLL_'].update_animation(resource_path('rick.gif'),time_between_frames=250)
            Thread(target=rick_roll,daemon=True).start()

#Create original window (change "black" to "lightgreen" for light mode)
create_main_window('',(400,0),'black','','Featured',[0])
driver.quit()