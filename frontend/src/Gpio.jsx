import './Gpio.css'

import React, { useState, useEffect } from 'react';

function Gpio(){
    const [gpioState, setGpioState] = useState(0)

    useEffect(() => {
        fetch('http://127.0.0.1:5000/api/digital/output',{
        method: 'GET',
        headers: {     "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "'*'"  },
        })
          .then(response => response.json())
          .then(json => setGpioState(json.DQ1))
          .catch(error => console.error(error));
      }, []);

      const handleClick = async () => {
        fetch('http://127.0.0.1:5000/api/digital/output',{
          method: 'POST',
          body: JSON.stringify(
            {
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
        
    }

    return (
    <>
    <div className='address'>Q0.1</div>
    <div className='state'>{gpioState}</div>
    <button onClick={handleClick} >Toogle</button>
    </>
    )
}

export default Gpio;