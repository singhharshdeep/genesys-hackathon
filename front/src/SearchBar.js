import React, { Component } from 'react'
import axios from 'axios'
export default class SearchBar extends Component {

    state = {
        search:''
    }

    onChange = e => this.setState({[e.target.name] : e.target.value});     

    onSubmit=(e)=>{
        e.preventDefault();
        const headers = {
            'Content-Type':'application/json',
            'organizationid':'e2242208-c200-4b57-af40-9e855461cec7',
            'token':sessionStorage.getItem('token')
          }
        console.log(this.state.search);
        const kbId='78982621-302a-4f71-a358-6732325edd9f'
        let data= { "query":this.state.search,
                    "pageSize": 5,
                    "pageNumber": 1,
                    "sortOrder": "string",
                    "sortBy": "string",
                    "languageCode":"en-US",
                    "documentType": "Faq"
        }
        axios.post(`https://api.genesysappliedresearch.com/v2/knowledge/knowledgebases/${kbId}/search`, data, {headers:headers}).then(res=>
           {
            console.log(res);
            
           })
    }

    generateToken=()=>{
        
            const headers = {
                'organizationid':'e2242208-c200-4b57-af40-9e855461cec7',
                'secretkey':'11b1af90-7ebf-4418-a3eb-7e34ba756c84'
              }
          
              axios.post('https://api.genesysappliedresearch.com/v2/knowledge/generatetoken', {}, {
                headers: headers
              }).then(res=>
               {
                console.log(res.token);
                 sessionStorage.setItem('token',res.data.token)
               })
            }
    
    componentDidMount(){
        setInterval(()=> this.generateToken(), 3600000)
    }
    render() {
        return (
            <div className='card col-md-8'>
                 <form className="form" onSubmit={this.onSubmit}>
                <input className="form-control m-3" type="text" placeholder="Search"  name ='search' aria-label="Search"  value={this.state.name} onChange={this.onChange}/>
                <button className=" btn blue-gradient m-3 btn-md" type="submit" style={{color:'white'}}>Search</button>
                </form>
            </div>
        )
    }
}
