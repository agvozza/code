# Putting the camera guide online

The `a6000-guide` folder is the whole web app. It holds the guide, the home-screen icon, and the
offline helper. It only needs to go online once. These steps use Netlify, which is free.

## 1. Put it online (about 5 minutes, on a computer)

1. Download `a6000-guide.zip` and unzip it. You should have a folder called `a6000-guide` with
   6 files in it: `index.html`, `sw.js`, `manifest.webmanifest`, and three icon `.png` files.
2. Go to **app.netlify.com/drop** and sign up (free; "Sign up with email" is fine).
   Sign up **before** uploading. A site uploaded without an account is deleted after an hour.
3. Drag the **`a6000-guide` folder** onto the page.
4. After a few seconds you'll get a link like `https://random-words-123.netlify.app`.
5. Optional: to get a nicer link, go to **Site configuration → Change site name** and type something
   like `camera-guide-europe`. The link becomes `https://camera-guide-europe.netlify.app`.

## 2. Check it on your own iPhone

1. Open the link in **Safari**. It must be Safari, not the Gmail or Instagram in-app browser.
2. Tap **Share** (the square with the arrow) → scroll down → **Add to Home Screen** → **Add**.
3. Open the new **Camera Guide** icon on your home screen. It should open full screen, with no
   address bar.
4. Try it: tap a few tabs, search for "battery", and tap a result.
5. Offline test: turn on **Airplane Mode**, close the app (swipe it away), open it again from the
   icon. It should still open and work. Turn Airplane Mode off afterwards.

## 3. Send it to her

Copy this into iMessage, with your link in place of the example:

> Here's the guide for the camera 📷 https://camera-guide-europe.netlify.app
>
> Set it up before you leave (takes 30 seconds):
> 1. Open the link in Safari
> 2. Tap Share (square with the arrow) → Add to Home Screen → Add
> 3. Open the new Camera Guide icon once while you have Wi-Fi
>
> After that it works without signal. Start with Level 1 (Auto), and move up to Scenes and A mode when you feel like it!

Step 3 matters. The home-screen icon keeps its own offline copy, separate from Safari, and saves
it the first time she opens the icon with a connection.

## Changing the guide later

Ask Claude for the change, then on Netlify open your site → **Deploys** and drag the updated
`a6000-guide` folder onto the page. Her copy picks up the change the next time she opens the guide
with signal, and shows it the time after that.
