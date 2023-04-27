import React, { useState, useEffect } from 'react';
import './Search.css';


export default function Search() {
   
    const [groups, setGroups] = useState([]);
    const [users, setUsers] = useState([]);
    const [userSearchTerm, setUserSearchTerm] = useState('');
    const [groupSearchTerm, setGroupSearchTerm] = useState('');
    const userSearchResults = (
        <div>
          <h2>User Search Results:</h2>
          <ul style={{ listStyleType: "none" }}>
            {users.map((user) => (
              <li key={user[0]}>
                <h2>{user[1]} {user[2]}</h2>
              </li>
            ))}
          </ul>
        </div>
      );
    const groupSearchResults = 
    (
        <div>
          <h2>Group Search Results:</h2>
          <ul style={{ listStyleType: "none" }}>
            {groups && groups.map((group) => (
                    <li key={group[0]}>
                       <h2><a href={group[2]}>{group[1]}</a></h2>
                    </li>
            ))}
          </ul>
        </div>
      );

    function handleUserSearchSubmit(event) {
 
        event.preventDefault();
        console.log(`User searched for: ${userSearchTerm}`);

        fetch(`/search_user/${userSearchTerm}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ searchTerm: userSearchTerm })
          })
          .then(response => response.json())
          .then(data => {console.log(data);
            setUsers(data);
            console.log(users);})
          .catch(error => console.error(error));
    
          
    }   
    
    function handleGroupSearchSubmit(event) {
        event.preventDefault();
        console.log(`User searched for: ${groupSearchTerm}`);

        fetch(`/search_group/${groupSearchTerm}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ searchTerm: groupSearchTerm })
          })
          .then(response => response.json())
          .then(data => {
            console.log(data);
            setGroups(data);
            console.log(groups);
            
          })
          .catch(error => console.error(error));



      }
    //to build the button below I used html/css inspo from  https://www.w3schools.com/howto/howto_css_search_button.asp 
    //!!!!!need to add hyper link to user search result to redirect to their profile page
    return (
        <body>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"/>
            <h1>Search Spotify Social</h1>
            <form class="search" onSubmit={handleUserSearchSubmit}>
                <input type="text" placeholder="Search For Users..." value={userSearchTerm} onChange={event => setUserSearchTerm(event.target.value)} />
                <button type="submit"><i class="fa fa-search"></i></button>
            </form>
            {users.length > 0 && userSearchResults}
            <form class="search" onSubmit={handleGroupSearchSubmit}>
                <input type="text" placeholder="Search For Groups..." value={groupSearchTerm} onChange={event => setGroupSearchTerm(event.target.value)} />
                <button type="submit"><i class="fa fa-search"></i></button>
            </form>
            {groups.length > 0 && groupSearchResults}
     
            
           
    
      
       

        </body>
 
    );
  }