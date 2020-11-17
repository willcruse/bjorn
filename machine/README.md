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
On GET request gets the current config of the machine</br>
On POST request sets the config of the machine</br>
Methods: 'GET', 'POST'</br>
<b>TO BE IMPLEMENTED</b>

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
    "contents": [
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
