Installation
---
Currently, there is no release file because we don't want to publish it before paper submission.

Firefox: 
Visit `about:debugging` and install this add-on via "Load temporary Add-on" button.    
    

Chrome(or chromium):
Visit `chrome://extensions/` and enable "developer mode". Then install this add-on via "Load unpacked" button.

Usage
---
Extension will create a warning overlay on vulnerable answers if you are visiting any. For example visi this page:    
https://stackoverflow.com/questions/7724448/simple-json-string-escape-for-c

Data for extension is hard-coded inside extension to improve performance. You can examine it at `contentScripts/content.js` line 45 