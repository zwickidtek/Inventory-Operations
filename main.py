
def get_sku(string) -> str:
    tmp = string.split()
    return tmp[-1]

def get_emei(string) -> str:
    tmp = string.split()
    return tmp[1]

def sum_digits(n) -> int:
    a = 0
    while n > 0:
        a = a+n%10
        n=int(n/10)
    return a

def is_valid_emei(n) -> bool:
    int_imei = int(n)
    l = len(n)

    if l!=15:
        return False

    d = 0
    sum = 0
    for i in range(15,0,-1):
        d = (int)(int_imei%10)
        if i%2==0:
            d=2*d
        sum=sum+sum_digits(d)
        int_imei=int_imei/10
    return (sum%10==0)


# Read all the lines in the data file
with open('Python Coding Exercise Data 102622 (1)(1).txt') as file:
    lines = file.readlines()

# Loop over every send or receive operation indexing each one
inventory_index = {}
error_index = {}
count=0
fault_code_mapping = {}

for indx, string in enumerate(lines):
    # If the line is a send or receive operation
    if "RECV" in string or "SEND" in string:
        operation = "RECV" if "RECV" in string else "SEND"
        # Check for valid IMEI
        if not is_valid_emei(get_emei(string)):
            error_index[count] = "Invalid IMEI"
            count+=1
            continue
        # Assign the operation to the index with sku, emei, and list of faults
        inventory_index[count] = [operation, get_sku(string), get_emei(string)]
        for i in range(indx+1, len(lines)):
            if "RECV" in lines[i] or "SEND" in lines[i] or lines[i]=='\n':
                count+=1
                break
            else:
                # is a fault
                cleaned_str=lines[i].replace(' ', '')
                cleaned_str=cleaned_str.replace('\n', '')
                inventory_index[count].append(cleaned_str)
                numerical_code = ''.join([i for i in cleaned_str if i.isdigit()])
                fault = ''.join([s for s in cleaned_str if s.isalpha()])
                if numerical_code not in fault_code_mapping:
                    fault_code_mapping[numerical_code] = fault



# Provide the total number of devices that are currently at the partner, by SKU
inventory_count = {}
for order in inventory_index.values():
    operation = order[0]
    sku = order[1]
    if sku not in inventory_count and operation == "RECV":
        inventory_count[sku]=1
    elif sku in inventory_count and operation == "RECV":
        inventory_count[sku]+=1
    elif sku in inventory_count and operation == "SEND":
        inventory_count[sku]-=1


print('Inventory:')
for k, v in inventory_count.items():
    if v > 0:
        print(f'{k}: {v}')


# Provide a list of invalid records that are in the file including 1. why they are invalid 2. the record index
print('\n\nErrors:')
for k, v in error_index.items():
    print(f'{k} {v}')


# Provide a list of all the "Fault Codes" and their "Faults"
print('\n\nFault code mapping:')
for k,v in fault_code_mapping.items():
    print(f'{k} - {v}')




# 2. Design an SQL schema to store the data (i.e.: write the 'CREATE TABLE' DDL commands).

# CREATE TABLE `Operation`(
#     `id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
#     `operationType` VARCHAR(255) NOT NULL,
#     `IMEI` VARCHAR(255) NOT NULL,
#     `SKU` VARCHAR(255) NOT NULL,
#     `operationIndex` INT NOT NULL
# );

# CREATE TABLE `Invalids`(
#     `id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
#     `operationIndex` INT NOT NULL,
#     `reason` VARCHAR(255) NOT NULL
# );

# CREATE TABLE `Faults`(
#     `id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
#     `faultCode` INT NOT NULL,
#     `faultName` VARCHAR(255) NOT NULL,
#     `operationIndex` INT NOT NULL
# );