import './Gpio.css'

import React, { useState, useEffect } from 'react';

function Gpio(){
    const [gpioState, setGpioState] = useState(0)

    useEffect(() => {
        fetch('http://127.0.0.1:5000/api/digital/output',{
        method: 'POST',
        body: JSON.stringify(
          {
            "method": "GET",
            "ip_address": "192.168.1.95",
            "rack_number": 0,
            "port_number": 1,
            "db_number": 0,
            "start_address": 0,
            "value": 0
        }
        ),
        headers: {     "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "'*'"  },
        })
          .then(response => response.json())
          .then(json => setGpioState(json.value))
          .catch(error => console.error(error));
      }, []);

    return (
    <>
    <div className='address'>Q0.1</div>
    <div className='state'>{gpioState}</div>
    <button>Toogle</button>
    </>
    )
}

export default Gpio;