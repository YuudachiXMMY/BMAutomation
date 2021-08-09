<!-- vscode-markdown-toc -->
* 1. [Setup for Automation](#SetupforAutomation)
* 2. [Drivers](#spanidDriversDriversspan)
	* 2.1. [Steps](#Steps)
* 3. [Automation Scripts](#AutomationScripts)
* 4. [<span id="Installation">Installation Setup</span>](#spanidInstallationInstallationSetupspan)
* 5. [Scripts Development](#ScriptsDevelopment)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc --># AMD Automation

##  1. <a name='SetupforAutomation'></a>Setup for Automation

1. Follow all the steps in <a href="#Drivers">Driver</a> section.
2. **Copy**, **Paste** and **Install** all files under `\\crazystone.amd.com\Incoming\JasonWu\MyAPI\AMDAutomation\VITAL\vital`:
    * 7-Zip: `7z1900-x64.exe`
    * DDU: `DDU v18.0.1.5.exe`
    * TightVNC: `tightvnc-2.8.8-gpl-setup-64bit.msi`
        * Set all password to `amd123`
        * Record the IP and the machine name.
    * VC Redist: `vc_redist.x64.exe`
    * VS Runtime: `vsruntime-2005-2010-x86.exe`
    * DotNet: `dotNetFx35setup.exe`
    * AMD Tools:
        * `CFXPanel.exe`
        * `FindGPUDriver64_2016.09.21_v0.4.exe`
3. **Copy**, **Paste** and **Install** all necessary games _(Follow all the steps in <a href="#Installation">Installation Setup</a> section)_.
4. **Copy** and **Paste** and **Unzip** the latest automation script under `\\crazystone\Incoming\JasonWu\MyAPI\AMDAutomation\scripts\`
5. **Right-Click** on `app.exe` and **Run as Administrator** to start the automation.

##  2. <a name='spanidDriversDriversspan'></a><span id="Drivers">Drivers</span>

**Copy** and **Paste** the latest version of target Base Driver and DXXP Driver for tests.
Can be fond here: `\\crazystone\Incoming\JasonWu\MyAPI\AMDAutomation\drivers`.

###  2.1. <a name='Steps'></a>Steps

1. Use DDU to uninstall the base driver.
2. **Unzip** the target Base Driver, and click on the `Setup.exe` to install (Please follow the steps shown in the setup window).
3. After all the installation for Base Driver is done, use `FindGPUDriver64_2016.09.21_v0.4.exe` to open the Base Driver folder. Get the permission of the Base Driver Folder, and **Copy** and **Paste** the DXXP driver into that folder.
4. Open `CFXPanel.exe`, search for `OnPal 10` and set it to True.
5. You are ready to use DXXP to run games :)

##  3. <a name='AutomationScripts'></a>Automation Scripts

Latest: [AMDAutomation_2021.7.19.15.23.1.7z](\\crazystone.amd.com\Incoming\JasonWu\MyAPI\AMDAutomation\scripts\AMDAutomation_2021.7.19.15.23.1)

Can be found under `\\crazystone\Incoming\JasonWu\MyAPI\AMDAutomation\scripts\`

##  4. <a name='spanidInstallationInstallationSetupspan'></a><span id="Installation">Installation Setup</span>

Please read [`\\crazystone\Incoming\JasonWu\MyAPI\AMDAutomation\VITAL\README.MD`](.\VITAL\README.MD)

##  5. <a name='ScriptsDevelopment'></a>Scripts

Please run the following code in your command line first:

```
python -m pip install -r requirements.txt
```

[`\\crazystone.amd.com\Incoming\JasonWu\MyAPI\AMDAutomation\dev`](.\dev)
