<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      v-if="!['Login', 'Register'].includes($route.name)"
    >
      <div class="d-flex align-center">
        AtlasLabs Password Manager
      </div>
      <v-spacer></v-spacer>
      <v-btn>
        <router-link to="/">Home</router-link>
      </v-btn>
      <v-btn>
        <router-link to="/login">Login</router-link>
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>


export default {
  name: 'App',
}
</script>


