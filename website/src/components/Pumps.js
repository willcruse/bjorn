import { Card, CardBody, CardText, CardTitle} from "shards-react";

export function Pumps(props){

    return (
        <Card>
            <CardBody>
                <CardTitle>Pumps</CardTitle>
                {props.pumps.map((val) => <CardText key={val.contents}>{val.contents}</CardText>)}
            </CardBody>
        </Card>
    );
}

Pumps.defaultProps = {"pumps": []}