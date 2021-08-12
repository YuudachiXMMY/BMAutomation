
$time = Get-Date -Format 'yyyy.MM.dd.HH.mm.ss'
$folder_name = "AMDAutomation_$time"

$working_dir = Get-Location
$tar_dir = "$working_dir\examples\AMDAutomation\"

echo $tar_dir

cd $tar_dir
# cd .\examples\AMDAutomation\dev

# pyinstaller --distpath="./build/$folder_name" --workpath="./build/$folder_name" --specpath="./build/$folder_name" -i="$tar_dir\Huskies.ico" -F app.py
pyinstaller --distpath="./scripts/$folder_name" --workpath="./scripts/$folder_name" --specpath="./scripts/$folder_name" -i="$tar_dir\dev\Huskies.ico" -F "dev\app.py"

cd ../../

New-Item -Path $tar_dir/scripts/$folder_name -Name tinytask -type directory
Copy-Item $tar_dir/dev/tinytask/* $tar_dir/scripts/$folder_name/tinytask
Copy-Item $tar_dir/dev/tinytask/mouse/* $tar_dir/scripts/$folder_name/tinytask/mouse
Copy-Item $tar_dir/dev/config.json $tar_dir/scripts/$folder_name/config.json
