# EnvironmentSensor

## Run environment sensor python script
Set excecution privileges in the folder
```
chmod +x envsensor.py
```
Run it with nohup to prevent stopping when terminal is exited. The ```&``` means it will run in the background.
```
nohup python3 envsensor.py &
```
You can find the process and its process ID with this command:
```
ps -fA | grep python
```

To terminate the script run
```
kill PID
```
