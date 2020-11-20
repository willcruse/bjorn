import { useEffect, useState } from "react";
import { 
    Card, 
    CardBody, 
    CardTitle, 
    Form, 
    FormGroup, 
    FormInput, 
    FormSelect, 
    Button 
} from "shards-react";

export function Make(props){
    
    const [currentDrink, setCurrentDrink] = useState();
    const [amount, setAmount] = useState(0);

    useEffect(() => {
        if (props.drinks.length > 0) {
            setCurrentDrink(props.drinks[0].name)
        }
    }, [props.drinks])
    return (
        <Card>
            <CardBody>
                <CardTitle>Make</CardTitle>
                <Form>
                    <FormGroup>
                        <label htmlFor="#drink-name">Drink</label>
                        <FormSelect 
                            id="#drink-name"
                            value={currentDrink}
                            onChange={(event) => {setCurrentDrink(event.target.value)}}
                        >
                            {props.drinks.map(value => {
                                return (
                                    <option 
                                        key={value.name} 
                                        value={value.name}
                                    >
                                        {value.name}
                                    </option>)
                                }
                            )};
                        </FormSelect>
                    </FormGroup>
                    <FormGroup>
                        <label htmlFor="#amount">Amount (ml)</label>
                        <FormInput 
                            id="#amount" 
                            type="text" 
                            onChange={(event) => {setAmount(event.target.value)}}
                            invalid={isNaN(amount)}
                        />
                    </FormGroup>
                </Form>
                <Button disabled={props.pouring} onClick={() => {props.makeHandler(currentDrink, amount)}}>Make</Button>
            </CardBody>
        </Card>
    );
}

Make.defaultProps = {
    "drinks": [],
    "makeHandler": () => {console.warn("makeHandler prop not set")},
    "pouring": false
}