# 018 QO-100  Some problems to solve  And a gift from my wife (Part 5)

- URL: https://youtu.be/IAONzZUyEQc
- Uploaded: 20220323  |  Length: 8:12
- Source: YouTube auto-captions (lightly cleaned; expect mis-heard words)

## Description

Cross-posted video from my main channel (Because it is HAM related)

In this video series, we are building a ground station for a geostationary satellite and trying to talk to a guy in Antarctica. It is a bonus series and not directly related to the regular topics of the channel.
The last two weeks were rainy and wet here in Switzerland. I have the antenna outside, and I did not want to go there with my delicate equipment. That is why I still was not able to transmit a signal and receive my voice from space. But I was not lazy!
And I got a gift from my wife...

Newest product links in this video: https://youtu.be/-kftVbNo8yo

Links (also from other QO-100 videos:
QO-100: Playlist: https://www.youtube.com/playlist?list=PL3XBzmAj53RnbYBRvlmuPyp24S4jfBrb5
POTY instruction: https://youtu.be/BVLgaoNW9uA
POTY antenna: https://www.passion-radio.com/satellite-qo-100/poty-antenna-762.html
Adalm Pluto SDR Receiver: https://amzn.to/3fSQPxk
PLL LNBs: https://www.passion-radio.com/satellite-qo-100/124
Green LNB (good for external clock modification): https://ebay.to/2WV3reR
Pre-amplifier: https://s.click.aliexpress.com/e/_dUe4N89
20W amplifier: https://s.click.aliexpress.com/e/_dWLz3oH
8W amplifier:  https://s.click.aliexpress.com/e/_dZtezNn or https://amzn.to/2SKoBLv
Power Meter: https://s.click.aliexpress.com/e/_Bfg8e1xF or https://amzn.to/35FNdtV
SMA torque wrench: https://s.click.aliexpress.com/e/_d7oR2yh or https://amzn.to/2zeEG5b
50W Attenuator (not tested): https://s.click.aliexpress.com/e/_dZAOLLB
GPSDO Leo Bodnar: http://www.leobodnar.com/shop/index.php?main_page=product_info&products_id=234
Filter design: https://rf-tools.com/lc-filter/
Adalm Pluto Hack: https://tbspace.de/plutosdrclockinput.html
LNB Hack: https://ea3cno.wordpress.com/2019/09/23/lnb-con-referencia-externa/
K3NG Keyer: https://github.com/k3ng/k3ng_cw_keyer
Begali keys (Say hello to Bruna from me): https://www.i2rtf.com/signature.html with black finish and optional blue paddles

The links above usually are affiliate links that support the channel (no additional cost for you). 
Github: https://www.github.com/sensorsiot 
My Patreon Page: https://www.patreon.com/AndreasSpiess 
If you want to support the channel, please use the links below to start your shopping. No additional charges for you, but I get a commission (of your purchases in the next 24 hours) 
My Amazon.com shop: https://www.amazon.com/shop/andreasspiess 
For Banggood https://bit.ly/2jAQEf4 
For AliExpress: http://bit.ly/2B0yTLL For Amazon.de: http://amzn.to/2r0ZCYI 
For Amazon UK: http://amzn.to/2mxBaJf For ebay.com: http://ebay.to/2DuYXBp 
https://twitter.com/spiessa As an Amazon Associate, I earn from qualifying purchases

## Transcript

in this video series we are building a ground station for a geostationary satellite and try to talk to a guy in antarctica this is a bonus series and not directly related to the regular topics of this channel it is strongly suggested to start watching at the beginning of the playlist now showing in the top right gritsy youtubers here is the guy with the swiss accent with a new episode and fresh ideas around sensors and microcontrollers remember if you subscribe you will always sit in the first row the last two weeks were rainy and wet here in switzerland i have the antenna outside and i did not want to go there with my delicate equipment that is why i still was not able to transmit a signal and receiving my voice from space but i was not lazy i built a 25 megahertz filter for the local oscillator i played dentist and pulled a crystal out of the lnb it did not hurt i added the reference signal injection path to the lnb i assembled the whole station on a wood port reprogrammed the addon pluto to work with a 25 megahertz reference and maybe killed one of them so let's start if you remember we need a stable 25 megahertz local oscillator signal for the lnb and the sdr receiver needs a stable 40 megahertz clock signal i decided to buy this gpsdo from leobotner because it has two outputs but this device delivers a square waveish signal not a sine wave because it uses a quartz crystal the original oscillator in the lnb produces a sine wave so how can we transform a square wave into a sine the solution is simple if we look at the spectrum of the square wave it has harmonics at megahertz 75 megahertz and even higher frequencies if we were able to filter these harmonics we would have a pure sine wave but how can we build such a filter easy peasy google is your best friend and you find for example this page we want a low pass filter which does not hurt all frequencies below 25 megahertz but kills everything above it so low pass 25 megahertz cutoff and 50 ohms on both sides are evident but the rest for example the type these names sound very exotic which one to choose it does not matter too much for this application so we choose butterworth maybe because of sympathy with our british colleagues which suffered a lot because of corona order four standard values and e12 because i do not want to wind the coils myself by the way what is e12 it is a system of preferred numbers for electronic components and consists of 12 values per decade you immediately recognize it because all our resistors for example are numbered like that there are also e24 e48 and even e96 series available but already an e24 series of resistors needs a lot of space this is why i only have an e12 series of smd capacitors resistors and inductances now we press compute and get a beautiful drawing of our filter and also this curve relevant for us is s21 which is the attenuation between input and output it is around 2.5 db at 25 megahertz and 36 db at 75 megahertz the 50 megahertz harmonics anyway was smaller and therefore needs a little less attenuation with this filter we should get a decent sine wave and here is the result all soldered under the binocular connected to the spectrum analyzer we see a similar curve as simulated the attenuation at 75 megahertz is a little lower than expected but still okay and if we insert the filter into the gp sdo signal we get a nearly pure sine wave cool so we should be able to insert it into the lnb next i had to take out the crystal and add a possibility to inject the 25 megahertz into the lnb i used this twin lnb and desorted one of its outputs i found this small network to inject the signal and i used through-hole components because i think it is easier to solder them in place ready is the lnb i hope i can test it next week the weather forecast is promising i also found that we can change the reference frequency of the addon pluto using this command just copy paste if i choose 25 megahertz i can use a single frequency gpsdo in the future for the lnb and the sdr the signal produced by the original oscillator in the pluto is around 2.2 volts and we have to match it more or less using attenuators and it is somehow square so we do not need a filter for this path now it was time to put all components in place i used the wood board concept where i glue the main parts in place and connect them using coax and other cables i also added a power distribution box for 12 volts and because this project is closely related to rockets i thought i add an appropriate main switch let's look at the connections and start with the pluto the rx path currently is quite simple just the bias t which inserts the 12 volts to power the lnb maybe later i have to add an attenuator because the signal from the lnb is quite strong the transmission path goes via the pre-amplifier to the power amplifier and to the potty antenna one channel of the gpsto is connected to the atom pluto and the other via the filter is connected to the lnb unfortunately my modified addon pluto stopped working with sdr console it is still visible on the computers though i hope i did not fry one of the chips during my extended experiments one last thing here is the gift of my wife for two hundred thousand subscribers it is a yambik here from begali a beautiful piece of mechanics in an otherwise electronics lab long time subscribers know that i once was a radio telegrapher for the red cross with age i found out that morse is like driving a bicycle if you were able to do it once on a certain level you do not lose it it only gets rusty because the keyer does not produce a tone i had to build this beautiful clear project from k3 ng now i hear what i keep pure nostalgia maybe i will be able to do my first qso with it on qo100 as always you find all the relevant links in the description i hope this video was useful or at least interesting for you if true please consider supporting the channel to secure its future existence thank you
