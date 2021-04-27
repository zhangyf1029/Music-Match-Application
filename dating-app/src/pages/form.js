import React from 'react'

function form() {
  return (
    <html>
        <head>
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.2/css/bulma.min.css"/>
        </head>
        <body>
            <form method="POST" action="/signup" enctype="multipart/form-data">
                <div class="field">
                    <div class="control">
                        <input class="input is-large" type="email" name="email" required value="{{userinfo.email}}" placeholder="Email" autofocus=""/>
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <input class="input is-large" type="text" name="first_name" required value="{{userinfo.display_name}}" placeholder="First Name" autofocus=""/>
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <input class="input is-large" type="text" name="last_name" required placeholder="Last Name" autofocus=""/>
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <input class="input is-large" type="text" name="pronouns" required placeholder="pronouns" autofocus=""/>
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <input class="input is-large" type="text" name="preferences" required placeholder="preferences" autofocus=""/>
                    </div>
                </div>
                <div class="field">
                    <div class="control">
                        <input class="input is-large" type="date" name="dob" placeholder="Date of Birth" autofocus=""/>
                    </div>
                </div>

                <div class="field">
                    <div class="control">
                        <input class="input is-large" type="password" name="password" placeholder="Password"/>
                    </div>
                </div>

                <input type="hidden" name="token" value="{{token}}"/>
                <input type="hidden" name="refresh_token" value="{{refresh_token}}"/>



                <button class="button is-block is-info is-large is-fullwidth">Sign Up</button>
            </form>
        </body>
    </html>
  )
}

export default form
