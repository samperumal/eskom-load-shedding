<template>
  <div class="wrapper">
    <p v-if="loading">Loading...</p>
    <b-table v-if="people.length > 0" :data="people" :columns="columns" backend-sorting backend-pagination></b-table>
  </div>
</template>

<script>
import Vue from "vue";
import Component from "vue-class-component";
import axios from "axios";

@Component
export default class TableTest extends Vue {
  people = [];
  loading = false;
  columns = [
    {
      field: "name",
      label: "Name"
    },
    {
      field: "birth_year",
      label: "Birth Year"
    }
  ];

  mounted() {
    this.loading = true;
    axios
      .get("https://swapi.co/api/people/")
      .then(response => {
        this.loading = false;
        this.people = response.data.results;
      })
      .catch(error => {
        this.loading = false;
        console.log(error);
      });
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.wrapper {
  margin: 2em;
}
</style>
