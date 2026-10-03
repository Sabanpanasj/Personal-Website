# Portfolio resume website (Python + Netlify)

Dark theme, amber accents, a photo behind your name, and a floating bottom menu (Home, About, Projects, Skills, Contact).

## 1. Add your details
- Open `resume_data.py` and replace the placeholder text (name, email, phone, school, skills, projects, social usernames).
- Your photo is in `assets/profile.jpg`. To use a different photo, replace that file (or change `PHOTO` in `resume_data.py`). A PNG with a transparent background also works well. With no photo you get a soft blue glow.
- The "Download Resume" button only appears when the file `assets/resume.pdf` exists.
  - Already have a resume? Save it as `assets/resume.pdf`.
  - No resume yet? Run `pip install -r requirements.txt` once, then `python make_resume.py`. It creates `assets/resume.pdf` from your details in `resume_data.py`. Run it again whenever you change your details.
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

## 3b. Deploy on Cloudflare Pages instead of Netlify
1. Run `python build.py` so the `dist` folder is up to date.
2. Sign in at https://dash.cloudflare.com and create a Pages project with **Direct Upload** (drag and drop).
3. Name the project and drag the whole `dist` folder (or a zip of it) into the upload box, then click Deploy.
4. Your site will be at `your-project-name.pages.dev`.
5. `netlify.toml` is not used on Cloudflare, and **Netlify Forms do not work there**. Use the Web3Forms key in `resume_data.py` (see Option B below) so the contact form emails you.
6. To update the site later, run `python build.py` again and upload the new `dist` folder to the same project.

## 3c. Put it on GitHub and deploy automatically
1. Create a new repository on GitHub (for example `resume-website`).
2. Upload the CONTENTS of this folder (README.md, build.py, resume_data.py, `dist`, `assets`, and the other files) so they sit at the top level of the repository. Or use the terminal:
```
git init
git add .
git commit -m "My resume website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/resume-website.git
git push -u origin main
```
3. In Cloudflare: Workers & Pages > Create application > Pages > Connect to Git. Choose your repository.
4. Framework preset: None. Build command: leave blank. Build output directory: `dist`. Click Save and Deploy.
5. To update the site later: edit `resume_data.py`, run `python build.py`, then commit and push. Cloudflare redeploys by itself.

The `dist` folder must be in the repository, because Cloudflare uploads what is inside it.

## 4. Get messages in your email (Netlify only)
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

## Popup notifications
The site shows small popup notifications (like Alertify) at the top right: green when your message is sent, red if it fails, blue when the resume starts downloading. They close by themselves after a few seconds, or when clicked.
To try one, open your site, press F12, click Console, and type: `notify("Hello!", "success")`
Types: `success`, `error`, `warning`, `message`. A third number sets the seconds, for example `notify("Hi", "warning", 10)`.

## Facebook, Instagram and TikTok
Websites cannot send messages into these apps automatically, so the round icons link to them:
- Facebook opens a Messenger chat with you
- Instagram opens a DM to you
- TikTok opens your profile
