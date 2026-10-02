# Portfolio resume website (Python + Netlify)

Dark theme, amber accents, a photo behind your name, and a floating bottom menu (Home, About, Projects, Skills, Contact).

## 1. Add your details
- Open `resume_data.py` and replace the placeholder text (name, email, phone, school, skills, projects, social usernames).
- Your photo is in `assets/profile.jpg`. To use a different photo, replace that file (or change `PHOTO` in `resume_data.py`). A PNG with a transparent background also works well. With no photo you get a soft blue glow.
- The "Download Resume" button only appears when the file `assets/resume.pdf` exists.
  - Already have a resume? Save it as `assets/resume.pdf`.
  - No resume yet? Run `pip install reportlab` once, then `python make_resume.py`. It creates `assets/resume.pdf` from your details in `resume_data.py`. Run it again whenever you change your details.
  - After either step, run `python build.py` again (or `python serve.py`).
- Project pictures (optional): save them in `assets/` and set `"image": "assets/project1.png"` in `resume_data.py`.

## 2. Test on your computer
```
python serve.py
```
Your browser opens at http://localhost:8000. Refresh the page after editing `resume_data.py` and the changes show up right away. Press Ctrl+C in the terminal to stop.

The contact form shows the "Message sent" page and prints the message in the terminal, but it does not send a real email. Real emails start working after you deploy on Netlify.

To use another port: `python serve.py 3000`

### Test on your phone or tablet
1. Connect the phone to the same Wi-Fi as your computer.
2. Run `python serve.py` and look for the line "On your phone (same Wi-Fi): http://...".
3. Type that address into the phone's browser.

To keep the test private to your computer only, run `python serve.py --local-only`.

The site adjusts to phones, tablets, laptops and large screens. On small screens the menu shows icons only, and the active section shows its name.

## 3. Deploy on Netlify

**Important:** upload the whole project, not just `index.html`. If you drag and drop, drag the whole `dist` folder (it holds `index.html`, `thanks.html` and the `assets` folder with your photo). If you use GitHub, upload every file in this folder, including `netlify.toml`.

1. Upload this folder to a GitHub repository.
2. In Netlify: Add new site > Import an existing project > choose the repository.
3. Netlify reads `netlify.toml` (build command `python build.py`, publish folder `dist`). Click Deploy.

## 4. Get messages in your email
1. Netlify > your site > Forms. After the first deploy you will see a form called `contact`.
2. Site configuration > Notifications > Form submission notifications > Add notification > Email notification.
3. Enter your personal email, choose the `contact` form, and save. Then send yourself a test message.

## Option B: free Web3Forms (if Netlify Forms does not work for you)
1. Go to https://web3forms.com, type your personal email, and submit. Your access key is sent to that email.
2. Open `resume_data.py` and paste the key between the quotes: `WEB3FORMS_KEY = "your-key-here"`
3. Run `python serve.py`, send a test message, and check your inbox (and spam folder).
4. Redeploy the `dist` folder on Netlify.

With a key set, messages go through Web3Forms instead of Netlify Forms. Leave the key empty to use Netlify Forms.
The key is visible in the page source. That is normal for this service; it only lets people send messages to your inbox.

## Facebook, Instagram and TikTok
Websites cannot send messages into these apps automatically, so the round icons link to them:
- Facebook opens a Messenger chat with you
- Instagram opens a DM to you
- TikTok opens your profile
