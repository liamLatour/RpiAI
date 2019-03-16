import urllib.request as urllib2
import html2text
import re
import numpy as np
import json
from scipy.optimize import curve_fit

try:
    import matplotlib as matplot
    matplot.use('Agg')
    import matplotlib.pyplot as mpl
    plottingEnabled = True
except:
    print("Matplotlib not detected, plotting disabled")
    plottingEnabled = False
  
def normpdf(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


def count_occurences(context, sentence):
    sentence = sentence.lower()
    occurences = 0
    words_in_sentence = len(sentence.split())
    for word in context['context_words']:
        if words_in_sentence < context['hasFewerWordsThan'] or words_in_sentence > context['hasMoreWordsThan']:
            occurences = occurences + sentence.count(word)
            # If spaces are important, use: occurences = occurences + sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), sentence))
    if occurences > 0 and context['hasSpecial'] in sentence:
        occurences = occurences *2
    return occurences

def get_url_markdown(baseurl):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0')]
    j = opener.open(baseurl)
    data = j.read()
    print(data)

    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.body_width = 10000
    return h.handle(data.decode('utf8'))
  


def get_occurrences(contexts,text):
    o_array = {}
    x = np.array([0])
    for context in contexts:
        o_array[context] = np.array([0])

    line_number = 0
    for line in text.splitlines():
        line_number = line_number + 1
        x = np.append(x,[line_number])
        print(str(line_number) + ":\t",)
        for i in contexts:
            num_occurences = count_occurences(contexts[i],line.strip())
            print(str(num_occurences) + "\t",)
            o_array[i] = np.append(o_array[i],[num_occurences])
        print(line)
    return o_array

def calculate_context_peaks(contexts,o_array):
    if plottingEnabled:
        fig = mpl.figure()
    contextNum = 0
    o_fits = {}
    for context in contexts:
        yi=np.array([])
        xi=np.array([])
        a=o_array[context]
        for i in np.arange(1,len(a)-5,5):
            yi = np.append(yi,np.sum(a[i:i+5]))
            xi=np.append(xi,i+3)
        for i in np.arange(2,len(a)-5,5):
            yi = np.append(yi,np.sum(a[i:i+5]))
            xi=np.append(xi,i+3)
        for i in np.arange(3,len(a)-5,5):
            yi = np.append(yi,np.sum(a[i:i+5]))
            xi=np.append(xi,i+3)
        for i in np.arange(4,len(a)-5,5):
            yi = np.append(yi,np.sum(a[i:i+5]))
            xi=np.append(xi,i+3)
        for i in np.arange(5,len(a)-5,5):
            yi = np.append(yi,np.sum(a[i:i+5]))
            xi=np.append(xi,i+3)
        
        #popt, pcov = curve_fit(normpdf, x, y)
        bestArea = 0
        for i in range(1,o_array[context].size):
            try:
                popt, pcov = curve_fit(normpdf, xi, yi, p0=[np.max(yi)/2,i,3])
                if popt[0]*0.5*popt[2] > bestArea and popt[2]<15:
                    bestArea = popt[0]*0.5*popt[2]
                    best_popt = popt
                    best_pcov = pcov
            except:
                pass
        popt = best_popt
        o_fits[context] = popt
        pcov = best_pcov
        if plottingEnabled:
            ym = normpdf(xi, popt[0], popt[1], popt[2])
            ax = fig.add_subplot(100*len(contexts)+11+contextNum)
            ax.scatter(xi, yi,label=context)
            ax.plot(xi, ym, c='r', label='Best fit')
            mpl.title(context)
            mpl.ylabel('Contextual density')
        contextNum = contextNum + 1
    if plottingEnabled:
        mpl.xlabel('Line number')
        fig.savefig('ingredients.png')
    return o_fits

def get_snippets(contexts,baseurl):
    print("Getting url " + baseurl + "...")
    text = get_url_markdown(baseurl)
    print("Getting number occurences in each line...")
    o_array = get_occurrences(contexts,text)
    print("Curve fitting on single gaussian...")
    o_fits = calculate_context_peaks(contexts,o_array)
    print("Grabbing snippets...")
    o_snippet = {}
    for context in o_fits:
        o_snippet[context] = ""
        
    line_number = 0
    for line in text.splitlines():
        line_number = line_number + 1
        for context in o_fits:
            if line_number >= o_fits[context][1]-round(2*o_fits[context][2]) and line_number <= o_fits[context][1]+round(2*o_fits[context][2]):
                if len(line)>1 and "##" not in line:
                    o_snippet[context] = o_snippet[context] + line + "\n"
            
    return o_snippet

baseurl = 'http://www.foodnetwork.com/recipes/alton-brown/baked-macaroni-and-cheese-recipe.html'
baseurl = 'http://tastykitchen.com/recipes/main-courses/sour-cream-chicken-enchilada-casserole/'
baseurl = 'http://www.foodnetwork.com/recipes/alton-brown/basic-waffle-recipe.html'
contexts = json.load(open('context_settings.json','r'))
snippets = get_snippets(contexts,baseurl)  
for context in snippets:
    print("-"*30)
    print(context)
    print("-"*30)
    print(snippets[context])
    print("\n\n")