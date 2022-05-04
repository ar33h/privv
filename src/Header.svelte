<script>
  import { username, user } from './user';

  function signout() {
    user.leave();
    username.set('');
  }
</script>

<header>
<h1> </h1>
  {#if $username}
    <div class="user-bio">
      
      <!-- <img class="image" src={`https://avatars.dicebear.com/api/initials/${$username}.svg`} alt="avatar" />  -->
      <span>Welcome <strong>{$username}</strong></span>
      
    </div>

    <button class="signout-button" on:click={signout}>Sign Out</button>

    {:else}

      <h3> </h3>
  {/if}
</header>