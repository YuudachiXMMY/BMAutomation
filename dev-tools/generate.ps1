cd .\examples\AMDAutomation\dev

$time = Get-Date -Format 'yyyy.MM.dd.HH.mm.ss'

$folder_name = "AMDAutomation_$time"
$working_dir = "C:\Users\Navi\Desktop\BMAutomation\examples\AMDAutomation\dev"

pyinstaller --distpath="./build/$folder_name" --workpath="./build/$folder_name" --specpath="./build/$folder_name" -i="$working_dir\Huskies.ico" -F app.py

New-Item -Path ./build/$folder_name -Name tinytask -type directory
Copy-Item ./tinytask/* ./build/$folder_name/tinytask
Copy-Item ./config.json ./build/$folder_name/config.json

cd ..\..\..\