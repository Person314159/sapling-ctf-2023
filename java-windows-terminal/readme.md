## `Java Windows Terminal`
### Problem Description
- Author: vEvergarden
    - We found this hidden website attached with a note, but we can't find our flag! The note said something about JWTs... Java Windows Terminal? Jim Wolf Technology? Either way, we also found a script lying around on the computer. Maybe you'll know what to do with it...

### Solution
The first thing I googled was "ctf RSA find private key given public key" and literally the first link was https://github.com/RsaCtfTool/RsaCtfTool. Downloaded it, ran `RsaCtfTool.py` on `public.key`, and what do you know, it cracked the private key in about a minute:

https://user-images.githubusercontent.com/26018590/216798066-93d22cbd-1ca2-4987-b5ab-c5d85dd0dc54.mp4

Only after I cracked it with the tool did I realize that `p` and `q` in `generate_keys.py` were suspiciously close 🤦

After that, I tried logging in to http://jwt.ctf.maplebacon.org:8000/login, and yeeted the cookie once I logged in:

![](java-windows-terminal-1.png)

Paste it into https://jwt.io/, pasted the public/private key, changed the payload to `"user": "admin"`, then fiddle around with it more to get the flag.

![](java-windows-terminal-2.png)

![](java-windows-terminal-3.png)

### Flag: `maple{f3rm4t_!n_7h3_m0d3rn_w0r1d}`
