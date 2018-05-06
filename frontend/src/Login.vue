<template>
  <div id="app" :class="`page ${currentRouteName}-page`">
    <router-view/>
  </div>
</template>

<script>

export default {
  name: 'Login',
  computed: {
    currentRouteName () {
      return this.$route.name
    }
  }
}
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css?family=Raleway');
@import './assets/scss/login.scss';
</style>