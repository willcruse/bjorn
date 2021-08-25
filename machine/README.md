# Cocktail Machine Software

## API

### Route: '/'
Tells you to refer to documentation on API usage</br>
Methods: 'GET'</br>

### Route '/make'
Makes \<amount> of drink. Blocks until finished pouring</br>
Methods: 'POST'</br>
Request JSON:
```
{
    "drink_name": "DRINK_KEY",
    "amount": AMOUNT_TO_POUR
}
```
Reponse JSON:</br>
On success:
```
{
    "success": true
}
```
On failure:</br>
```
{
    "error": "ERROR_MESSAGE"
}
```

### Route '/config'
On GET request gets the config file of the machine</br>
On POST request sets the config of the machine</br>
Methods: 'GET', 'POST'</br>
GET:</br>
On success:
```
{
    "success": true
    "pumps": [
        {
            "type": PUMP_TYPE,
            "config": {
                "contents": DRINK_TYPE,
                "pins": [PIN_NUMBERS]
            }
        }
    ]
}
```
On failure:
```
{
    "error": "ERROR_MESSAGE"
}
```
POST:</br>
`number`: is the pump number to modify (corresponds to array index)</br>
Request JSON:
```
{
    pumps: [
        {
            number: PUMP_NUMBER,
            type: PUMP_TYPE 
            config: {
                contents: DRINK_TYPE, 
                pins: [PIN_NUMBERS] 
            }
        }
    ]
}
```
On success:
```
{
    pumps: [
        {
            number: PUMP_NUMBER,
            type: PUMP_TYPE
            config: {
                contents: DRINK_TYPE,
                pins: [PIN_NUMBERS]
            }
        }
    ]
}
```
On failure:
```
{
    "error": "ERROR_MESSAGE"
}
```

### Route '/drinks'
Fetches all stored drinks on the machine</br>
Methods: 'GET'</br>
On success:
```
{
    "success": true
    "drinks": [
        {
            "name": DRINK_NAME,
            "contents": [
                [INGREDIENT, AMOUNT]
            ]
        }
    ]
}
```
On failure:
```
{
    "error": "ERROR_MESSAGE"
}
```

### Route '/add-drink'
Adds a new drink to storage
Methods: 'POST'</br>
Request JSON:
```
{
    "name": DRINK_NAME,
    "components": [
        [INGREDIENT, AMOUNT]
    ]
}
```

On success:
```
{
    "success": true
}
```
On failure:
```
{
    "error": "ERROR_MESSAGE"
}
```

### Route '/delete-drink'
Removes a drink from the database
Methods: 'POST'</br>
Request JSON:
```
{
    "name": DRINK_NAME,
}
```
On success:
```
{
    "success": true
}
```
On failure:
```
{
    "error": "ERROR_MESSAGE"
}
```

### Route '/random'
Creates a random mixture
Methods: 'POST'</br>
Request JSON:
```
{
    "amount": AMOUNT_TO_POUR
}
```
On success:
```
{
    "success": true
}
```
On failure:
```
{
    "error": "ERROR_MESSAGE"
}
```
