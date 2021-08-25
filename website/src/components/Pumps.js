import { Card, CardBody, CardText, CardTitle} from "shards-react";

export function Pumps(props){

    return (
        <Card style={{minWidth: "18rem"}}>
            <CardBody>
                <CardTitle>Pumps</CardTitle>
                {props.pumps.map((val) => <CardText key={val.config.contents}>{val.config.contents}</CardText>)}
            </CardBody>
        </Card>
    );
}

Pumps.defaultProps = {"pumps": []}