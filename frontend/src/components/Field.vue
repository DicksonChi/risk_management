<template>
  <div>
    <!-- form here to add a new Risk Item-->
    <modal v-if="isAddFieldModalVisible">
      <h3 slot="header" class="modal-title">
        Add Field To List
      </h3>

      <div slot="body">
        <form @submit="SubmitAddFieldModal">
          <div class="form-group">
            <label for="name">Name</label>
            <input
              type="text"
              class="form-control"
              placeholder="Field"
              id="name"
              v-model="name"
              required
            />
          </div>
         
          <div class="form-group">
           <label class="typo__label">Field Type</label>
            <multiselect v-model="field_type" :options="options" :searchable="true" :close-on-select="true" :show-labels="false" placeholder="Select a type">
              <template slot="selection"></template>
            </multiselect>
          </div>
          <label v-if="field_type == 'ENUM'"
            title="Please you are required to enter the value"
            >Options</label
          ><br />
          <div class="form-group "  v-if="field_type == 'ENUM'">
            <div
              class="row"
            >
              <input
                type="text"
                placeholder="option one"
                class="form-control"
                v-model="option_one"
              />
            </div>
            <div
              class="row"
            >
              <input
                type="text"
                placeholder="option two"
                class="form-control"
                v-model="option_two"
              />
            </div>
            <div
              class="row"
            >
              <input
                type="text"
                placeholder="option 3"
                class="form-control"
                v-model="option_three"
              />
            </div>
          </div>
          <div class="form-group">
            <button type="submit" class="btn btn-outline-info">Add</button>
            <button
              type="button"
              class="btn btn-outline-info"
              @click="closeAddRiskTypeModal"
            >
              close
            </button>
          </div>
        </form>
      </div>
    </modal>
    <button
      class="btn btn-lg"
      title="add a new field"
      @click="showAddRiskTypeModal"
    >
      Add Field <i class="fa fa-plus"></i>
    </button>

    <div class='tag-input'>
      <div v-for='field in fields' :key='field.id' 
      class='tag-input__tag'>
        {{ field.name }} ({{ field.field_type }})
      </div>
    </div>
    <br/>
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import modal from "./modal/Modal.vue";
import { APIService } from "../BackendApiService.js";

export default {
  name: "Fields",
  components: {
    Multiselect,
    modal
  },
  props: ["fields"],
  
  methods: {
    showAddRiskTypeModal() {
      this.isAddFieldModalVisible = true;
    },
    closeAddRiskTypeModal() {
      this.isAddFieldModalVisible= false;
    },
    SubmitAddFieldModal(e) {
      e.preventDefault();
      let api_serv = new APIService();
      const field = {
        name: this.name,
        field_type: this.field_type,
        options_data: {
          option_one: this.option_one,
          option_two: this.option_two,
          option_three: this.option_three 
        
        }
      };
      api_serv
        .createField(field)
        .then(res => {
          if (res.data.code == "010") {
            this.$emit("update-field");
            this.name = "";
            this.field_type = "";
          }
        })
        .catch(err => {
          console.log(err);
        });
      this.isAddFieldModalVisible = false;
    },
    // other JS methods here
  },
  data() {
    return {
      isAddFieldModalVisible: false,
      name: "",
      field_type: "",
      options:['TEXT', 'NUMBER', 'DATE', 'ENUM'],
      option_one: "",
      option_two: "",
      option_three: ""
    };
  }
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
.btn {
  border-color: rgb(21, 156, 235);
  color: rgb(21, 156, 235);
  margin: 5px;
}
.btn:hover {
  background-color: rgb(21, 156, 235);
  color: white;
}
.tag-input {
  width: 100%;
  border: 1px solid #eee;
  font-size: 0.9em;
  height: 50px;
  box-sizing: border-box;
  padding: 0 10px;
}

.tag-input__tag {
  height: 30px;
  float: left;
  margin-right: 10px;
  background-color: #eee;
  margin-top: 10px;
  line-height: 30px;
  padding: 0 5px;
  border-radius: 5px;
}

.tag-input__tag > span {
  cursor: pointer;
  opacity: 0.75;
}
</style>
