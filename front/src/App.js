import React from 'react';
// import '@fortawesome/fontawesome-free/css/all.css';
import SearchBar from './SearchBar'
import {useEffect} from 'react'
import axios from 'axios'

function App() {


  useEffect(() => {
    
    // const headers = {
    //   'organizationid':'e2242208-c200-4b57-af40-9e855461cec7',
    //   'secretkey':'11b1af90-7ebf-4418-a3eb-7e34ba756c84'
    // }
    
    // axios.post('https://api.genesysappliedresearch.com/v2/knowledge/generatetoken',{
    //   headers
    // }).then(res=>
    //  {

    //    console.log(res)
    //  })
   
  })
  return (
    <div className="App center" >
    <div className='col-md-6 offset-md-3 mt-3'>
     <SearchBar/>
     </div>
    </div>
  );
}

export default App;
