import winreg

REG_PATH = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000"
REG_NAMES = [r"D3DVendorName", r"D3DVendorNameWoW"]
REPLACE_VALUES = [r"atidxx64.dll", r"atidxx32.dll"]
newValues = [[],[]]

# Loop through the two keys
for i, REG_NAME in enumerate(REG_NAMES):
    # Open the key on the loop index with QUERY access, get the Multi-String and reg type, and close it
    registry_key_read = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_QUERY_VALUE)
    values, regType = winreg.QueryValueEx(registry_key_read, REG_NAME)
    winreg.CloseKey(registry_key_read)

    # Loop throgh the values
    # We only want to update the last 2 values, to keep DX9NAVI but disable DX11NAVI
    for j, value in enumerate(values):
        if(j > 1):
            # Replace the last value of the dir with the new file
            parts = value.split('\\')
            parts[-1:] = [REPLACE_VALUES[i]]
            newValue = '\\'.join(parts)
            newValues[i].append(newValue)
        else:
            newValues[i].append(value)
    
    # Open the key on the loop index again, but with SET access, set the new Multi-String, and close it
    registry_key_write = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(registry_key_write, REG_NAMES[i], 0, regType, newValues[i])
    winreg.CloseKey(registry_key_write)

    print(f'Key {i+1} of 2 updated!')