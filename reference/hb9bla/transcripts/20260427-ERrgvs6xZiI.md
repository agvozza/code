# Programmable Signal Generator for Receiver Testing

- URL: https://youtu.be/ERrgvs6xZiI
- Uploaded: 20260427  |  Length: 6:31
- Source: YouTube auto-captions (lightly cleaned; expect mis-heard words)

## Description

We are developing an 80-meter direction finder, and I wanted to test it automatically. For that, I needed a remotely controlled RF generator.
But I did not want to spend a lot of money. Including everything, the cost should remain well below $ 50 (Aliexpress).

Links:
SI5351 unshielded: https://de.aliexpress.com/item/32915414654.html or https://amzn.to/3Ox2d8C
SI5351 shielded: https://s.click.aliexpress.com/e/_c39uU9wR or https://amzn.to/3Ox2d8C
PE4302 unshielded: https://de.aliexpress.com/item/4000143116674.html or https://amzn.to/4ucyl0c
PE4302 shielded: https://s.click.aliexpress.com/e/_c2vl1ccf or https://amzn.to/4ucyl0c
SMA Attenuators: https://s.click.aliexpress.com/e/_c3VUpi0R or https://amzn.to/4uhnB0P
Variable 60-90dB max attenuator: https://s.click.aliexpress.com/e/_c3B5QjJ1 or https://amzn.to/4ucyl0c

Project: https://github.com/SensorsIot/Universal-Embedded-Workbench

The links above are usually affiliate links that support the channel (at no additional cost to you). 
GitHub: https://www.github.com/sensorsiot 
My Patreon Page: https://www.patreon.com/AndreasSpiess 
If you want to support the channel, please use the links below to start your shopping. No additional charges for you, but I get a commission (on your purchases in the next 24 hours) 
My Amazon.com shop: https://www.amazon.com/shop/andreasspiess 
For Banggood https://bit.ly/2jAQEf4 
For AliExpress: http://bit.ly/2B0yTLL For Amazon.de: http://amzn.to/2r0ZCYI 
For Amazon UK: http://amzn.to/2mxBaJf For ebay.com: http://ebay.to/2DuYXBp 
https://twitter.com/spiessa 
As an Amazon Associate, I earn from qualifying purchases

## Transcript

We are developing a 80-meter direction finder and I wanted to test it automatically. For that, I needed a remotely controlled RF generator. But I did not want to spend a lot of money. Including everything, the cost should stay well below $50. Hello wireless enthusiasts. Here is the channel with a strange twist distortion in the signal with a new video around wireless and other exciting stuff. Make sure you subscribe if you do not want to miss the following emissions. This little RF generator consists of only four main parts, a Raspberry Pi Zero and SI5351 clock generator module, a PE4302 digital attenuator module, and a few fixed attenuators. The Raspberry Pi could be replaced by an even cheaper ESP32. Then the budget would fall below $20. The useful frequency range is from about 8 kHz to 160 MHz. So it can cover many amateur radio bands from LF and HF up to VHF. But we have to remember one important thing. The SI5351 produces a square wave-like signal, not a clean sine wave. This means it also produces harmonics. For serious measurements, we need filtering, shielding, and calibration. But for practical receiver checks, it is already a very useful little tool. The Raspberry Pi Zero controls the SI5351 over I²C and sets the desired frequency. The RF signal then goes through the PE4302 attenuator. This attenuator can digitally reduce the signal level by up to 31.5 dB in 0.5 dB steps and it also is controlled by the Pi. This makes the generator repeatable. For my 80-meter direction finder, I can set the frequency to around 3.5 MHz and then reduce the signal step by step and see how the receiver behaves. I can check whether the receiver hears the signal, whether the S meter reacts plausibly, and where the squelch or weak signal limits starts. For the automatic test, I connected the direction finder's earphone output through a low-pass filter and a diode to a GPIO pin on its controller. Yes, this will be a very modern direction finder with Wi-Fi and smartphone user interface, including QR code camera input for the frequencies of the foxes. But there is one very important point. The PE4302 alone is not enough for real receiver sensitivity tests. The receiver sensitivity is usually tested with very small signals. For example, a signal of 1 microvolt into 50 ohms is about minus 107 dBm. A signal of 0.1 microvolt is approximately minus 127 dBm. So we need additional attenuation. I use a 20 dB attenuator between the SI5351 and the PE4302 and additional fixed attenuators after the PE4302 if needed. To get a measurable signal, I check the level with an oscilloscope before the last attenuator and then I calculate the power using this formula. Where VRMS is the voltage in volts across 50 ohms. My raw generator's output is around 800 mV RMS or 10 dBm on 50 ohms. If you want to test a receiver at minus 120 dBm, we need about 130 dB attenuation. The PE4302 gives us about 30 dB. If we also use a fixed 20 dB attenuator before it, we need around 80 dB of additional fixed attenuation after the PE4302. So the basic rule is simple. Use fixed attenuators to bring the signal down into the microvolt range and use the PE4302 for convenient variable attenuation. Of course, the Pi can also create Morse signals if you want to hear the signal quality directly. As said before, the setup is not a replacement for a calibrated laboratory signal generator. The output waveform is not perfect, the absolute level needs calibration, and shielding and filtering matter. But it is cheap, programmable, repeatable, and very useful in the ham shack. And because I used the AI agent Claude code to control it, I even get ready-made Excel curves as output, extremely fast. As usual, you find the link to the open-source Raspberry Pi code in the video description along with links to the boards and attenuators I use. The code includes additional functionality such as serial connections for debugging ESP32 modules. But this is stuff for another video. And you can use the Pi also without the two modules. Then it creates a 3.3 V square signal at one of its GPIOs. Of course, also with Morse if you wish. And if you want a much better signal source, you can upgrade to something like an AD9959 DDS module. It offers a cleaner sine wave output and more possibilities, but also at a very different price tag. That's all for today. As always, you find all the relevant links in the description. 73 to everybody and please consider supporting the channel using the links in the description. See you in the next episode.
