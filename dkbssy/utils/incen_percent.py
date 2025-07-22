import time


def inc_percent_amt_calc(cat):
    percentage = None
    if cat == 'अधिष्ठाता अस्पताल अधीक्षक ,सहायक अधीक्षक नोडल अधिकारी एवं सहायक नोडल अधिकारी , अस्पताल  सलाहकार  ':
        percentage = .01
    elif cat == 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , ( फैकल्टी एंड रेसीडेंट )':
        percentage = .14
    elif cat == 'पैथोलॉजी ,रेडियोलॉजी , माइक्रोबायोलॉजी , बायोकेमेस्ट्री , निश्चेतना (टेक्निशियन )':
        percentage = 0.06
    elif cat == 'सभी फिजिशियन / सर्जन ':
        percentage = .45
    elif cat == 'सभी सीनियर एवं जूनियर रेसिडेंट ':
        percentage = .1
    elif cat == 'एनेस्थीसिया':
        percentage = .1
    elif cat == 'नर्सिंग एवं पैरामेडिकल स्टाफ ':
        percentage = .06
    elif cat == 'चतुर्थ वर्ग एवं सफाई कर्मचारी':
        percentage = .03
    elif cat == 'डाटा एंट्री ऑपरेटर':
        percentage = .05
    return percentage





def case_cycle(casear):
    all_casear = []
    casear = casear.split('\n')
    for c in casear:
        if c == '':
            pass
        else:
            # print('xxxx', c)
            cc = c.split('\t')
            all_casear.append(cc[0])
    return all_casear



