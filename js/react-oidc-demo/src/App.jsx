import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import React from "react";
import { AuthProvider, useAuth } from "react-oidc-context";
import './App.css'


const oidcConfig = {
  authority: "http://localhost:8080", // Replace with your OIDC provider's URL
  client_id: "QQFWLIWIVWIALRAEWGZXHCAGVGMUYYLGPPXEGRYIODUNQYHE", // Replace with your OIDC client ID
  redirect_uri: "http://localhost:5173/callback", // Replace with your Vite dev server URL
  post_logout_redirect_uri: "http://localhost:5173/",
  response_type: "code",
  scope: "openid profile email", // Adjust scopes as needed
  onSigninCallback: () => window.history.replaceState({}, document.title, window.location.origin)
}


function ProtectedContent() {
  const [count, setCount] = useState(0)
  const oidc = useAuth();

  return (
    <>
      <div>
        <button
          style={{
            position: "fixed",
            top: "10px",
            right: "10px",
          }}
          onClick={() => oidc.signoutRedirect()}>Logout</button>;
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}


function LoginButton() {
  const oidc = useAuth();

  if (oidc.isLoading) return <p>Loading...</p>;
  console.log(oidc)
  if (oidc.isAuthenticated)
    return <ProtectedContent />

  return <button onClick={() => oidc.signinRedirect()}>Login</button>;
}

function UserProfile() {
  // const oidcUser = useOidcUser();

  // if (!oidcUser) return null;

  // return (
  //   <div>
  //     <h2>User Profile</h2>
  //     <pre>{JSON.stringify(oidcUser.profile, null, 2)}</pre>
  //   </div>
  // );
}

export default function App() {
  return (
    <AuthProvider {...oidcConfig}>
      <div>
        <h1>React OIDC Demo</h1>
        <LoginButton />
      </div>
    </AuthProvider>
  );
}
