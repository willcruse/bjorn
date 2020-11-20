import { Card, CardBody, CardTitle, Form, FormGroup, FormInput, Button } from "shards-react";

export function Settings(props){

    return (
        <Card>
            <CardBody>
                <CardTitle>Settings</CardTitle>
                <Form>
                    <FormGroup>
                        <label htmlFor="#machine-address">Address</label>
                        <FormInput 
                            id="#machine-address" 
                            type="text" 
                            onChange={(event) => {props.updateAddress(event.target.value)}}
                            invalid={!isValidIP(props.machineAddress)}
                            value={props.machineAddress}
                        />
                    </FormGroup>
                    <FormGroup>
                        <label htmlFor="#port-number">Port</label>
                        <FormInput 
                            id="#port-number" 
                            type="text" 
                            onChange={(event) => {props.setPort(event.target.value)}}
                            invalid={isNaN(props.port)}
                            value={props.port}
                        />
                    </FormGroup>
                </Form>
                <Button onClick={props.connectHandler}>Connect</Button>
            </CardBody>
        </Card>
    );
}

export function isValidIP(address) {
    const ipRegex = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
    const matched = address.match(ipRegex);
    return matched !== null;
};

Settings.defaultProps = {
    "machineAddress": "",
    "updateAddress": () => {console.warn("updateAddress prop not set")},
    "connectHandler": () => {console.warn("connectHandler prop not set")},
    "setPort": () => {console.warn("setPort prop not set")},
    "port": "",
    "pumps": []
}
