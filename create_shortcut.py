import os

desktop = r"C:\Users\Shivr\Desktop"
proj_dir = os.path.dirname(os.path.abspath(__file__))
vbs_content = f'''Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{desktop}\\MudraAI.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{os.path.join(proj_dir, 'LAUNCH_MUDRAAI.bat')}"
oLink.WorkingDirectory = "{proj_dir}"
oLink.Description = "Launch MudraAI Live Website"
oLink.IconLocation = "shell32.dll,220"
oLink.Save
'''

vbs_file = os.path.join(proj_dir, "make_lnk.vbs")
with open(vbs_file, "w") as f:
    f.write(vbs_content)

os.system(f'cscript //nologo "{vbs_file}"')
if os.path.exists(vbs_file):
    os.remove(vbs_file)

print("Desktop icon created successfully!")
