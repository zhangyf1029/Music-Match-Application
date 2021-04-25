  
import React from "react";
import { List, Header } from "semantic-ui-react";

export const Users = ({ users }) => {
  return (
      <div>{users}</div>
    // <List>
    //   {users.map(users => {
    //     return (
    //       <List.Item key={users.email}>
    //         <Header>{users.first_name}</Header>
    //       </List.Item>
    //     );
    //   })}
    // </List>
  );
};
export default Users;