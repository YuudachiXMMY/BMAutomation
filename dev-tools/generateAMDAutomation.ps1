
$time = Get-Date -Format 'yyyy.MM.dd.HH.mm.ss'
$folder_name = "AMDAutomation_$time"

$working_dir = Get-Location
$tar_dir = "$working_dir\examples\AMDAutomation\scripts"

cd $tar_dir
# cd .\examples\AMDAutomation\dev

# pyinstaller --distpath="./build/$folder_name" --workpath="./build/$folder_name" --specpath="./build/$folder_name" -i="$tar_dir\Huskies.ico" -F app.py
pyinstaller --distpath="./build/$folder_name" --workpath="./build/$folder_name" --specpath="./build/$folder_name" -i="$tar_dir\Huskies.ico" -F app.py

cd ../../../

New-Item -Path $tar_dir/build/$folder_name -Name tinytask -type directory
Copy-Item $tar_dir/tinytask/* $tar_dir/build/$folder_name/tinytask
Copy-Item $tar_dir/tinytask/mouse/* $tar_dir/build/$folder_name/tinytask/mouse
Copy-Item $tar_dir/config.json $tar_dir/build/$folder_name/config.json
