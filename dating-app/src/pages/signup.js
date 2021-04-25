import React from 'react';

// export const Users = ({ users }) => { return (<div>{movies.length}</div> ) }

const Signup = () => {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '90vh'
      }}
    >
    {/* <h1 class="title">
        Music Match
    </h1> */}
    <h2 class="subtitle">
        Let your music play matchmaker today. 
    </h2>
    <div class="column is-4 is-offset-4">

        <form method="GET" action="5000/authspotify">
            <button class="button is-block is-info is-large is-fullwidth">Sign Up With Spotify</button>
        </form>

    </div>
    </div>
  );
};

export default Signup;