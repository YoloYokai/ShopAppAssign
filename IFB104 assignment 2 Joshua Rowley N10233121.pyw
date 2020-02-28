
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: N10233121
#    Student name: Joshua Rowley
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Online Shopping Application
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for simulating an online shopping experience.  See
#  the instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.
#

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.)
from tkinter import *

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#-----Downloader Function--------------------------------------------#
#
# This is our function for downloading a web page's content and both
# saving it on a local file and returning its source code
# as a Unicode string. The function tries to produce
# a meaningful error message if the attempt fails.  WARNING: This
# function will silently overwrite the target file if it
# already exists!  NB: You should change the filename extension to
# "xhtml" when downloading an XML document.  (You do NOT need to use
# this function in your solution if you choose to call "urlopen"
# directly, but it is provided for your convenience.)
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html'):
    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists!)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding = 'UTF-8')
        text_file.write(web_page_contents)
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_file + "'")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# Name of the invoice file. To simplify marking, your program should
# generate its invoice using this file name.
invoice_file = 'invoice.html'

#load webbrowser to make the program easier to use
from webbrowser import open_new

#set variables to global so they can be referenced inside functions 
global category,shop_list,cart_list,font_type

#set variables to place holder values
master = Tk()
cart_list = []
shop_list = []
master.title("Tech Traders")
window_state = 0
items_per_list=10
font_type=("Helvetica",13)
spinbox_font_type=("Helvetica",20)
category = IntVar()

#to give more variety on the items available 
from random import choice
randomise_url = ['?p=1&s=displayPrice&sd=1&fm=false',"",'?p=1&s=displayPrice&sd=2&fm=false','?p=1&s=displayName&sd=1&fm=false','?p=1&s=displayName&sd=2&fm=false']

#url's that are used later on 
url1 = 'https://www.jbhifi.com.au/games-consoles/games/gaming-headsets/'
url2 = 'https://www.jbhifi.com.au/games-consoles/accessories/gaming-mice/'
url3 = 'https://www.jbhifi.com.au/computers-tablets/gaming-pcs/'+choice(randomise_url)
url4 = 'https://www.jbhifi.com.au/games-consoles/games/pc-gaming/'+choice(randomise_url)


#loads the title, price and picture data fromf the urls
def parse_url(url,amount=items_per_list):
    web_doc = urlopen(url)
    web_doc_bytes = web_doc.read()
    web_doc_decoded = web_doc_bytes.decode('UTF-8')
    web_doc.close()
    product_list = []

    start_tag = '<div class="span03 product-tile" title="'
    end_tag = '<sup>'
    start =web_doc_decoded.find(start_tag)+len(start_tag)
    end = web_doc_decoded.find(end_tag,start)
    count = 0
    #loads all product information up to 10 products
    while start != -1 and end != -1 and count < amount:
        product_info = web_doc_decoded[start:end]
    #grab the 3 elements 
        cost = product_info[product_info.rfind('</span>')+7:]
        name = product_info[:product_info.find('">')]
        photo = product_info[product_info.find('data-src-retina="'):product_info.find('width="300" height="300" />')]
    #edit the cost to make it usable
        cost = cost.replace(" ","")
        cost = cost.replace('\r','').replace('\n',"")
    #edit the name to make it usable because of some unicode present
        name = name.replace('&#39;',"'")
        name = name.replace('&quot;','')
        name = name.replace('&amp;','&')
    #edit the photo to make it referenceable
        photo = photo[17:len(photo)-2]
        photo = 'https://www.jbhifi.com.au'+photo
    #add all the info to a list 
        product_list += [[name,cost,photo]]
    #find the next product
        start =web_doc_decoded.find(start_tag,end)+len(start_tag)
        end = web_doc_decoded.find(end_tag,start)
    #add a count to the products found 
        count += 1
    return(product_list)
#fart
#loads the title, price and picture data from the saved Htmls
def parse_saved_html(target):
    web_doc = open("Stocktake/"+target)
    web_doc_decoded = web_doc.read()
    web_doc.close()
    product_list = []
    start_tag = '<div class="span03 product-tile" title="'
    end_tag = '<sup>'
    start =web_doc_decoded.find(start_tag)+len(start_tag)
    end = web_doc_decoded.find(end_tag,start)
    count = 0
    #loads all product information up to 10 products
    while start != -1 and end != -1 and count < 10:
        product_info = web_doc_decoded[start:end]
    #grab the 3 elements 
        cost = product_info[product_info.rfind('</span>')+7:]
        name = product_info[:product_info.find('">')]
        photo = product_info[product_info.find('data-src-retina="'):product_info.find('width="300" height="300" />')]
    #edit the cost to make it usable
        cost = cost.replace(" ","")
        cost = cost.replace('\r','').replace('\n',"")
    #edit the name to make it usable
        name = name.replace('&#39;',"'")
        name = name.replace('&quot;','')
        name = name.replace('&amp;','&')
    #edit the photo to make it referenceable
        photo = photo[17:len(photo)-2]
        photo = 'https://www.jbhifi.com.au'+photo
    #add all the info to a list 
        product_list += [[name,cost,photo]]
    #find the next product
        start =web_doc_decoded.find(start_tag,end)+len(start_tag)
        end = web_doc_decoded.find(end_tag,start)
    #add a count to the products found 
        count += 1
    return(product_list)

#creates the text layout for the store popup
def text_parser(data):
    text = ""
    item_number=0
    for element in data:
        item_number = item_number + 1
        text += '\n'+"#"+str(item_number)+" "+element[0]+'\n   $'+element[1]
    text= text[1:]
    return(text)

#load the website data
headsets_raw = parse_saved_html('headsets.html')
mice_raw = parse_saved_html('gaming-mice.html')
pcs_raw = parse_url(url3)
games_raw = parse_url(url4)

#update the text field 
def update():
    global category,shop_list,cart_list,t
    t.config(state=NORMAL)
    t.delete('1.0',END)
    #checks for each category and loads the text depending on it
    if category.get() == 0:
        t.insert(END,"Please select a category")
        shop_list=[]
    elif category.get() == -1:
        t.insert(END,"No item selected")
        shop_list=[]
    elif category.get() == 1:
        t.insert(END,text_parser(games_raw))
        shop_list=games_raw    
    elif category.get() == 2:
        t.insert(END,text_parser(mice_raw))
        shop_list=mice_raw
    elif category.get() == 3:
        t.insert(END,text_parser(pcs_raw))
        shop_list=pcs_raw
    elif category.get() == 4:
        t.insert(END,text_parser(headsets_raw))
        shop_list=headsets_raw
    elif category.get() == 5:
    	t.insert(END,cart_list)
    t.config(state=DISABLED)

#add items to the cart
def add_cart():
    global shop_list,cart_list
    if shop_list != []:
        cart_list = cart_list + [shop_list[int(s.get())-1]]
        cart_list = test_for_count(cart_list)

#remove an item from the cart
def remove_cart():
    global shop_list,cart_list,cart_item,t
    #ensures you cant remove from an empty cart
    if cart_list != []:
        if cart_list[int(cart_item.get())-1][3]==1:
            cart_list.remove(cart_list[int(cart_item.get())-1])
        else:
            cart_list[int(cart_item.get())-1][3] = int(cart_list[int(cart_item.get())-1][3])-1
    if cart_list==[]:
        popup_cart()
    else:
        total_price=0
        item_count=0
        cart_str=""
        #creates the text for the cart
        for element in cart_list:
            total_price += int(element[1])*int(element[3])
        for element in cart_list:
            item_count+=1
            cart_str += str(item_count) + ". " +str(element[3])+"x "+ str(element[0])+" $"+str(element[1])+"\n"
        cart_str+="The total price is $"+str(total_price)+" AUD"
        t.config(state=NORMAL)
        t.delete('1.0',END)
        t.insert(END,str(cart_str))
        t.config(state=DISABLED)

#test if a item has been added more than once and ads a quantity to the list 
def test_for_count(input_list):
    edited = []
    for element in input_list:
        element.append(1)
        is_there = False
        for a in range(len(edited)):
            if edited != []:
                if element == edited[a]:
                    number=a
                    is_there = True
        if is_there==True:
            edited[number][3]+=1
        else:
            edited += [element]
    return(edited)

#prints a html recipt 
def recipt():
	global cart_list
	total_price = 0
	# calculate total price
	for element in cart_list:
		total_price+=int(element[1])*int(element[3])
	recipt_html= open(invoice_file,'w')
	item_count=0
	recipt_html_text='<!DOCTYPE html><html>\n<!--headding-->\n<p style="text-align:center;"><img src="tech traders logo.gif" width="500" height="400" alt="Logo"></p>\n'
	recipt_html_text+='<h1 align="center">The total price comes to $'+str(total_price)+'AUD</h1>\n<h2 align="center">(prompt payment would be nice)</h2>"'
	recipt_html_text+='\n<table align= "center" style=" width:500px; height:250px; border: 5px solid black;border-collapse: collapse; padding: 10px; text-align: center;" rules="all">\n'
	for element in cart_list:
		item_count+=1
		recipt_html_text +='<!--Product name-->\n<tr><td><h1 align="center"><font size=20>'+str(element[3])+'x</font> '+str(element[0])+"</h1></td></tr>\n<!--Product picture-->\n"
		recipt_html_text +='<tr><td><img src="'+str(element[2])+'" alt="'+str(element[0])+'" width="200" height="200" style="margin:0px auto;display:block">\n<!--Price indication-->\n'
		recipt_html_text +='<p align="center" ><font size="8">$'+str(element[1])+'AUD</font></p></td></tr>\n\n'

	recipt_html_text += '</table>\n'
	#check if cart is not empty whether or not to load 
	if cart_list !=[]:
        #puts in the style information for the invoice table 
		recipt_html_text += """<p></p><style>.invoice-box {
	        max-width: 800px;
	        margin: auto;
	        padding: 30px;
	        border: 1px solid #eee;
	        box-shadow: 0 0 10px rgba(0, 0, 0, .15);
	        font-size: 16px;
	        line-height: 24px;
	        font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
	        color: #555;
	    }
	    
	    .invoice-box table {
	        width: 100%;
	        line-height: inherit;
	        text-align: left;
	    }
	    
	    .invoice-box table td {
	        padding: 5px;
	        vertical-align: top;
	    }
	    
	    .invoice-box table tr td:nth-child(2) {
	        text-align: right;
	    }
	    
	    .invoice-box table tr.top table td {
	        padding-bottom: 20px;
	    }
	    
	    .invoice-box table tr.top table td.title {
	        font-size: 45px;
	        line-height: 45px;
	        color: #333;
	    }
	    
	    .invoice-box table tr.information table td {
	        padding-bottom: 40px;
	    }
	    
	    .invoice-box table tr.heading td {
	        background: #eee;
	        border-bottom: 1px solid #ddd;
	        font-weight: bold;
	    }
	    
	    .invoice-box table tr.details td {
	        padding-bottom: 20px;
	    }
	    
	    .invoice-box table tr.item td{
	        border-bottom: 1px solid #eee;
	    }
	    
	    .invoice-box table tr.item.last td {
	        border-bottom: none;
	    }
	    
	    .invoice-box table tr.total td:nth-child(2) {
	        border-top: 2px solid #eee;
	        font-weight: bold;
	    }
	        
	        .invoice-box table tr.information table td {
	            width: 100%;
	            display: block;
	            text-align: center;
	        }
	    }
	    
	    }
	    </style>
		<body>
	    <div class="invoice-box">
	        <table cellpadding="0" cellspacing="0">
	            <tr class="heading">
	                <td>
	                    Item
	                </td>
	                <td>
	                    QTY
	                </td>
	                <td>
	                    Price
	                </td>
	            </tr>\n
	            """
        #adds items to the invoice list 
		for item in cart_list:
			recipt_html_text+='<tr class="item"><td>'+str(item[0])+'</td>\n'
			recipt_html_text+='<td>'+str(item[3])+'</td>\n'
			recipt_html_text+='<td>$'+str(item[1])+'</td></tr>\n'
		recipt_html_text += """<tr class="total">
                <td></td>
                <td></td>
                
                <td>"""
		recipt_html_text +="Total: $"+str(total_price)
		recipt_html_text += '</td></tr></table></div></body>'
    #adds hyperlinks at the ends
	recipt_html_text += '<font size="6">\n<p style="padding-left: 10px">Stocktake Items stocked from</p>\n'
	recipt_html_text += '<ul>\n<li><a href="'+url1+'"">Headsets</a></li>\n<li><a href="'+url2+'"">Gaming Mice</a></li>\n</ul>'
	recipt_html_text += '\n<p style="padding-left: 10px">Regular Items stocked from</p>\n'
	recipt_html_text += '<ul>\n<li><a href="'+url3+'">Gaming PCs</a></li>\n<li><a href="'+url4+'"">PC Games</a></li>\n</ul>\n</font>\n'
	recipt_html_text +="</html>"


	recipt_html.write(recipt_html_text)
	recipt_html.close()
	open_new(invoice_file)
    
	#save data to a database
	database_list=[]
	for element in cart_list:
		for i in range(element[3]):
			database_list+=[[element[0],element[1]]]
	connection = connect('shopping_cart.db')
	Cart_db = connection.cursor()
	Cart_db.execute("DELETE FROM ShoppingCart")
	for element in database_list:
		sql=''
		element[0]=element[0].replace("'","{")
		sql+="('"+str(element[0])+"',"+str(element[1])+")"
		sql="INSERT INTO ShoppingCart VALUES "+sql
		Cart_db.execute(sql)
	connection.commit()
	Cart_db.close()
	connection.close()

#creates the cart popup
def popup_cart():
    global shop_popup, window_state,cart_item,cart_list,font_type,spinbox_font_type,t
    #checks if the window has been opened already
    if window_state == 1:
        shop_popup.destroy()
        window_state = 0 	
    shop_popup=Toplevel()
    centre_window(625,165,350)
    window_state = 1
    t=Text(shop_popup,height=10,width=75,font=font_type)
    t.grid(column=1,row=0,rowspan=6)
    scrollbar = Scrollbar(shop_popup,command=t.yview,width=20)
    cart_str=""
    item_count=0
    total_price=0
    if cart_list==[]:
        cart_str = "Your cart is empty"
    else:
        for element in cart_list:
            total_price += int(element[1])*int(element[3])
        for element in cart_list:
            item_count+=1
            cart_str += str(item_count) + ". " +str(element[3])+"x "+ str(element[0])+" $"+str(element[1])+"\n"
        cart_str+="The total price is $"+str(total_price)+" AUD"
    t.insert(END,str(cart_str))
    t.config(state=DISABLED,yscrollcommand=scrollbar.set)
    scrollbar.grid(column=2,row=0,sticky="NSW",rowspan=6)
    if cart_list!=[]:
        centre_window(850,200,350)
        if len(cart_list)==1:
            Label(shop_popup,text="1",width=2,font=font_type).grid(column=3,row=2)
            cart_item=Spinbox(shop_popup,values=(1),width=2,font=spinbox_font_type)
            cart_item.grid(column=3,row=2)
        else:
            cart_item=Spinbox(shop_popup, from_=1, to=len(cart_list),font=spinbox_font_type,width=2)
            cart_item.grid(column=3,row=2)
        Button(shop_popup,text="Remove from cart",font=font_type,command=remove_cart).grid(column=3,row=3)

#creates the shop popup
def popup():
    global shop_popup, window_state,t,category,s,font_type,spinbox_font_type
    #checks if the window has been opened already
    if window_state == 1:
    	shop_popup.destroy()
    	window_state = 0 	
    shop_popup=Toplevel()
    if category.get() != 0:
        centre_window(740,175)
    else:
        centre_window(625,175)
    window_state = 1
    t=Text(shop_popup,height=10,width=75,wrap=WORD,font=("Helvetica",11))
    t.grid(column=1,row=0,rowspan=6)
    scrollbar = Scrollbar(shop_popup,command=t.yview,width=20)
    t.insert(END,'Please select a category')
    t.config(state=DISABLED,yscrollcommand=scrollbar.set)
    scrollbar.grid(column=2,row=0,sticky="NSW",rowspan=6)
    if not (category.get()==0 or category.get()==-1):
        s=Spinbox(shop_popup, from_=1, to=items_per_list,width=2,font=spinbox_font_type)
        s.grid(column=3,row=2)
        Button(shop_popup,text="Add to cart",command=add_cart,width=10,font=font_type).grid(column=3,row=3)
    update()

#centres the shop popup
def centre_window(w,h,x_offset=0,y_offset=0):
	global shop_popup,master
	ws = shop_popup.winfo_screenwidth()
	hs = shop_popup.winfo_screenheight()
	x = (ws/2) - (w/2)-x_offset
	y = (hs/2) - (h/2)-y_offset
	shop_popup.geometry('%dx%d+%d+%d' % (w, h, x, y))

#opens shop window based on which button is pressed
def pcgames():
    category.set(1)
    popup()
def mice():
    category.set(2)
    popup()
def computers():
    category.set(3)
    popup()
def headphones():
    category.set(4)
    popup()

#import image
logo = PhotoImage(file='tech traders logo.gif')

#tkinter main menu UI
Label(image=logo).grid(column=0,row=0,rowspan=11)

#define colours of the frames
frame_colour_stocktake="chocolate1"
frame_colour_updated="forest green"

#creates the smaller frames for each sub category
stocktake = Frame(master,bg=frame_colour_stocktake)
stocktake.grid(column=1,row=4,rowspan=4,columnspan=2,sticky='NSEW',pady=5)
updated_stock = Frame(master,bg=frame_colour_updated)
updated_stock.grid(column=1,row=0,rowspan=4,columnspan=2,sticky='NSEW',pady=5)

#creates elements for the stocktake section
Label(stocktake,bg=frame_colour_stocktake,font=font_type,justify=LEFT ,text="Old Stock").grid(column=1,row=0,sticky='NSEW')
Button(stocktake,text="Mice",font=font_type, command=mice,width=20).grid(column=1,row=1,sticky='NSEW',columnspan=2)
Button(stocktake,text="Headphones",font=font_type, command=headphones,width=20).grid(column=1,row=2,sticky='NSEW',columnspan=2)

#creates the elements for the updated stock section
Label(updated_stock,bg=frame_colour_updated,font=font_type,justify=LEFT ,text="Updated Stock").grid(column=1,row=1,sticky='NSEW')
Button(updated_stock,text="Computers",font=font_type, command=computers,width=20).grid(column=1,row=2,sticky='NSEW',columnspan=2)
Button(updated_stock,text="PC Games",font=font_type, command=pcgames,width=20).grid(column=1,row=3,sticky='NSEW',columnspan=2)

#creates extra cart buttons under the subcategories 
Button(master,text="Print recipt",command=recipt,font=font_type).grid(column=2,row=10,sticky='NSEW')
Button(master,text="Show Cart",command=popup_cart,font=font_type).grid(column=1,row=10,sticky='NSEW')
mainloop()
