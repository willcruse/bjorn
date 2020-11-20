import {useEffect, useState} from "react";
import {Container, Row, Col, Navbar, NavbarBrand, CardDeck} from "shards-react";
import {Drinks} from './components/Drinks.js';
import {Settings, isValidIP} from './components/Settings.js';
import {Make} from './components/Make.js';
import {Pumps} from './components/Pumps.js';

function App() {

  const [machineAddress, setAddress] = useState("10.0.0.10");
  const [port, setPort] = useState(5000);
  const [pumps, setPumps] = useState([]);
  const [drinks, setDrinks] = useState([]);
  const [pouring, setPouring] = useState(false);

  const connectHandler = () => {
    if (isValidIP(machineAddress)) {
      fetch(`http://${machineAddress}:${port}/drinks`, {
        mode: 'cors'
      }).then((response) => {
        return response.json();
      }).then((json) => {
        if (json.drinks) {
          setDrinks(json.drinks);
        }
      }).catch((err) => {
        console.warn(err);
      });
      fetch(`http://${machineAddress}:${port}/config`, {
        mode: 'cors'
      }).then((response) => {
        return response.json();
      }).then((json) => {
        if (json.pumps) {
          setPumps(json.pumps);
        }
      }).catch((err) => {
        console.warn(err);
      });
    }
  };

  const makeHandler = (currentDrink, currentAmount) => {
    if (isValidIP(machineAddress) && !isNaN(port)) {
      const toSend = {
        "name": currentDrink,
        "amount": currentAmount
      };
      setPouring(true);
      console.log(pouring);
      fetch(`http://${machineAddress}:${port}/make`, {
        mode: 'cors',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(toSend)
      })
      .then((response) => {
        return response.json();
      }).then((json) => {
        setPouring(false);
        if (json.success !== true) {
          console.warn(json);
        }
      }).catch((err) => {
        console.warn(err);
      });
    }
  };

  const addDrinkHandler = (name, components) => {
    const toSend = {
      "name": name,
      "components": components
    }
    fetch(`http://${machineAddress}:${port}/add-drink`, {
      mode: 'cors',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(toSend)
    })
      .then((response) => {
        return response.json();
      }).then((json) => {
        console.log(json);
        if (json.success === true) {
          connectHandler();
        } else {
          console.warn(json);
        }
      }).catch((err) => {
        console.warn(err);
      });
  };

  useEffect(connectHandler, [machineAddress, port]);

  return (
    <>
    <Navbar type="dark" theme="primary" expand="md">
        <NavbarBrand href="#">Bjorn</NavbarBrand>
      </Navbar>
    <Container id="app-container" style={{"marginTop": "1rem"}} fluid>
      <Row>
        <Col>
        <CardDeck>
          <Make 
            drinks={drinks}
            makeHandler={makeHandler}
            pouring={pouring}
          />
          <Pumps
            pumps={pumps}
          />
        </CardDeck>
        </Col>
        <Col>
          <Row><Drinks 
            drinks={drinks}
            addDrinkHandler={addDrinkHandler}
            pumps={pumps}
          /></Row>
          <Row>
            <CardDeck><Settings 
            machineAddress={machineAddress} 
            updateAddress={setAddress} 
            connectHandler={connectHandler}
            port={port}
            setPort={setPort}
            pumps={pumps}
            />
            </CardDeck>
            </Row>
        </Col>
      </Row>
    </Container>
    </>
  );
}

export default App;
