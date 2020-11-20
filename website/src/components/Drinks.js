import { useEffect, useState } from "react";
import { 
    Card, 
    CardBody, 
    CardTitle, 
    CardColumns, 
    ListGroup, 
    ListGroupItem, 
    ListGroupItemHeading,
    FormGroup,
    Form,
    FormInput,
    Button,
    CardSubtitle,
    FormSelect
} from "shards-react";

export function Drinks(props){

    return (
        <CardColumns fluid>
            {props.drinks.length > 0 ?
                props.drinks.map((val) => <Drink key={val.name} name={val.name} components={val.components}/>) :
                <NoDrinks />}
            <NewDrink addDrinkHandler={props.addDrinkHandler} pumps={props.pumps}/>
        </CardColumns>
    );
}

function NewDrink(props) {

    const firstValueOrEmpty = () => props.pumps.length > 0 ? (props.pumps[0]).contents : ""

    const [drinkName, setDrinkName] = useState("");
    const [componentName, setComponentName] = useState(firstValueOrEmpty())
    const [amount, setAmount] = useState(0);
    const [components, setComponents] = useState([]);

    const updateComponents = () => {
        const newComponent = [componentName, amount];
        if (!isNaN(amount)) {
            setComponents([...components, newComponent])
            setComponentName(firstValueOrEmpty());
            setAmount(0);
        }
    };

    const sendDrink = () => {
        props.addDrinkHandler(drinkName, components)
        setDrinkName("")
        setComponents([])
        setComponentName("")
        setAmount(0)
    }

    
    useEffect(() => {setComponentName(firstValueOrEmpty())}, [props.pumps])

    return (
        <Card>
            <CardBody>
                <CardTitle>New Drink</CardTitle>
                <Form>
                    <FormGroup>
                        <label htmlFor="#drink-name">Drink Name</label>
                        <FormInput 
                            id="#drink-name"
                            value={drinkName}
                            onChange={(event) => {setDrinkName(event.target.value)}}
                        />
                    </FormGroup>
                    <CardSubtitle style={{marginTop: '0.5rem'}}>Ingredients</CardSubtitle>
                    {components.map(val => <p key={val[0]}>{`${val[0]}: ${val[1]}`}</p>)}
                    <FormGroup>
                        <FormGroup>
                            <label htmlFor="#component-name">Ingredient</label>
                            <FormSelect 
                                id="#component-name"
                                value={componentName}
                                onChange={(event) => {setComponentName(event.target.value)}}
                            >
                                {props.pumps.map(val => <option key={val.contents}>{val.contents}</option>)}
                            </FormSelect>
                        </FormGroup>
                        <FormGroup>
                            <label htmlFor="#component-amount">Amount</label>
                            <FormInput 
                                id="#component-amount"
                                value={amount}
                                onChange={(event) => {setAmount(event.target.value)}}
                                invalid={isNaN(amount)}
                            />
                        </FormGroup>
                        <Button style={{marginTop: '0.5rem'}} onClick={updateComponents} disabled={componentName === ""}>Add Ingredient</Button>
                    </FormGroup>
                </Form>
                <Button onClick={sendDrink}>Add Drink</Button>
            </CardBody>
        </Card>
    )
}

function NoDrinks() {
    return (
        <Card>
            <CardBody>
                <CardTitle>{'No Drinks :('}</CardTitle>
            </CardBody>
        </Card>
    )
}

function Drink(props) {
    return (
        <Card>
            <CardBody>
                <CardTitle>{props.name}</CardTitle>
                <ListGroup>
                    {props.components.map(val => <Ingredient key={val[0]} contents={val[0]} amount={val[1]} />)}
                </ListGroup>
            </CardBody>
        </Card>
    )
}

const Ingredient = (props) => (
    <ListGroupItem>
        <ListGroupItemHeading>{props.contents}</ListGroupItemHeading>
    </ListGroupItem>
)


Drinks.defaultProps = {
    "drinks": [],
    "addDrinkHandler": () => {console.warn("addDrinkHandler was not passed as a prop")},
    "pumps": []
}

Drink.defaultProps = {
    "name": "",
    "components": []
}

Ingredient.defaultProps = {
    "contents": "",
    "amount": ""
}

NewDrink.defaultProps = {
    "addDrinkHandler": () => {console.warn("addDrinkHandler was not passed as a prop")},
    "pumps": []
}