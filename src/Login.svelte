<script>
  import { user } from './user';

  let username;
  let password;

  function login() {
    user.auth(username, password, ({ err }) => err && alert(err));
  }

  function signup() {
    user.create(username, password, ({ err }) => {
      if (err) {
        alert(err);
      } else {
        login();
      }
    });
  }
</script>
<center><img class="logo" src='./assets/logo.png' alt="Logo">
<!-- <label for="username">Username</label> -->
<input name="username" placeholder="Username" bind:value={username} minlength="3" maxlength="16" />
<br><br>
<!-- <label for="password">Password</label> -->
<input name="password" placeholder="Password" bind:value={password} type="password" />
<br><br>
<button class="login" on:click={login}>Login</button>

<h2 class="signup" on:click="{signup}"> New to Privv? Sign Up</h2>
</center>
<!-- <button class="login"  on:click={signup}>Sign Up</button> -->

<h2 class="footer"> Truly Indian 🇮🇳 </h2>
<h3 class="developed"> Developed by Arshdeep & Dhruval </h3>