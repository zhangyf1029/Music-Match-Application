import React from 'react';

const Start = () => {
  return (
    <html>
      <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css" />
      </head>
      <body>
        <section class="hero is-primary is-fullheight">
          <div class="hero-body">
            <div class="container has-text-centered">
              <h1 class="title">
                Connect with people around Boston
              </h1>
              <div class="column is-4 is-offset-4">
              <form method="GET" action="/signup">
                <button class="button is-block is-info is-large is-fullwidth">Start Now</button>
              </form>
              </div>
            </div>
          </div>
        </section>
      </body>
    </html>
    // <div
    //   style={{
    //     display: 'flex',
    //     justifyContent: 'center',
    //     alignItems: 'center',
    //     height: '90vh'
    //   }}
    // >
    //   <h1>We are aspiring entrepreneur.</h1>
    // </div>
  );
};

export default Start;