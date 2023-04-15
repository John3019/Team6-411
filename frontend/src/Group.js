
import React, { useState, useEffect } from 'react';
import './Group.css';
import './button-2.css';

export default function Group() {
    const [people, setPeople] = useState([]);
  
    useEffect(() => {
      let gid = 1;
  
      fetch(`/groupdata/${gid}`)
        .then(response => response.json())
        .then(data => {
          setPeople(data);
          console.log(data);
        })
        .catch(error => console.error(error));
    }, []);
  
    

  return (
    
    <body>
     
        <h1>Welcome to Group Z</h1>
        <h2> Leaderboard</h2>

        <div className="gtable">
            <table>
                <thead>
                <tr>
                    <th>Username</th>
                    <th>Top Song</th>
                    <th>Top Arist</th>
                    <th>Top Genre</th>
                    <th>Minutes Listened</th>
                    <th>Compatibility</th>

                </tr>
                </thead>
                <tbody>
  
                    {people && people.map((person, index) => (
                        <tr key={index}>
                            <td>{person.username}</td>
                            <td>{person.topsong}</td>
                            <td>{person.topartist}</td>
                            <td>{person.topgenre}</td>
                            <td>{person.minutes}</td>
                            <td>{person.compat}</td>
                        </tr>
                    ))}

                </tbody>
            </table>
            </div>
     
            <div class="button-container">
            <button className="button-2" type="button">Back to Profile</button>
            <button className="button-2" type="button">Send Invitation</button>
            </div>
    </body>
       
      
      
    
  );
}
