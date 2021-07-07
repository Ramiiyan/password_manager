<template>
  <div class="home">
    <v-container fluid fill-height >
      <v-alert type="error" :value="alert" dense>
        {{this.key_error}}
      </v-alert>
      <v-row justify="center" align="center">
        <v-col cols="8">
          <v-text-field
            v-model="m_key"
            label="Enter Master Key"
            clearable
            outlined
            :rules="[() => !!m_key || 'This field is required']"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="2">
          <v-btn class="ma-2" color="primary"
            :loading="btnloader" 
            :disabled="btnloader" 
            @click="submit"
          >
            Submit
            <template v-slot:btnloader>
              <span class="custom-loader">
                <v-icon light>mdi-cached</v-icon>
              </span>
            </template>
          </v-btn>
        </v-col>
      </v-row>
      <v-spacer></v-spacer>
      <div class="view_Actua_Data" v-if="this.viewData">
        {{this.dataList}}
        <v-data-table
          :headers="headers"
          :items="dataList"
          :items-per-page="10"
          class="elevation-1"
        ></v-data-table>

      </div>
      <v-fab-transition>
        <v-btn
          v-show="viewData"
          color="primary"
          dark
          absolute
          bottom
          right
          fab
          @click="add_data_dialog = true"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-fab-transition>
      <v-dialog v-model="add_data_dialog" persistent max-width="600">
        <v-card>
          <v-card-title class="text-h5">
            Add New Data
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-form ref="add_data_form">
              <v-row>
                <v-col cols="4" sm="4" md="4">
                  <v-text-field v-model="add_data.url" 
                    ref="url" label="URL" required 
                    :rules="[() => !!add_data.url || 'This field is required']"
                  ></v-text-field>
                </v-col>
                <v-col cols="4" sm="4" md="4">
                  <v-text-field v-model="add_data.username" 
                    ref="username" label="Username" required
                    :rules="[() => !!add_data.username || 'This field is required']"
                  >
                  </v-text-field>
                </v-col>
                <v-col cols="4" sm="4" md="4">
                  <v-text-field v-model="add_data.password" 
                    ref="username" label="Password" required
                    :rules="[() => !!add_data.password || 'This field is required']"
                  ></v-text-field>
                </v-col>
              </v-row>
              </v-form>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="black"
              text
              @click="add_data_dialog = false"
            >
              Close
            </v-btn>
            <v-btn
              color="blue darken-1"
              text
              @click="addData"
            >
              Save
            </v-btn>
          </v-card-actions>
        </v-card>
        <v-alert 
          :type="data_alert_type" :value="data_alert" dense>
          {{this.data_alert_msg}}
        </v-alert>
      </v-dialog>
    </v-container>
  </div>
</template>

<script>

export default {
  name: 'Home',
  components: {
    // HelloWorld
  },
  data: () => ({
    m_key: null,
    receivedData:null,
    user_id:null,
    btnloader:false,
    viewData:false,
    dataList:[],
    alert:false,
    key_error:null,
    add_data_dialog:false,
    add_data:{
        url:null,
        username:null,
        password:null
    },
    data_alert:false,
    data_alert_msg:null,
    data_alert_type:"error",
    headers:[
      { text:'URL', value:'url'},
      { text:'Username', value:'username'},
      { text:'Password', value:'password'},
    ]

  }),

  created(){
    this.receivedData = this.$route.params.data
    this.user_id = this.receivedData.userId
  },

  mounted(){
    if(alert){
      this.hide_alert();
    }
    if(this.data_alert){
      this.hide_data_alert();
    }
  },

  methods:{
    async submit(){
      const msg = {
        user_id:this.user_id,
        m_key:this.m_key
      }
      console.log(msg);
      if(this.m_key != null){
        await this.ValidateMasterKey("http://localhost:5000/validate_mkey", msg);
      }
      else{
        console.log("m_key field is null");
      }
    },

    async ValidateMasterKey(url, msg) {
      this.btnloader = true;
      return await this.axios({
        url: url,
        method: 'POST',
        // responseType: 'application/json',
        data: msg,
      }).then((res)=>{
        this.btnloader = false;
        console.log(res);
        var response = res.data.response;
        console.log(response);

        if(response == "success"){
          console.log("true");
          const decrypted_data = res.data.data_msg.dataList //list of data
          this.viewData = true;
          console.log(decrypted_data);
          this.decryptoData(decrypted_data);

        }else{
          this.alert=true;
          this.key_error = "Invalid Master Key"

        }
      })
    },

    decryptoData(dataList){
      for(var i=0; i<dataList.length; i++ ){
        // crpted_val -> decrypt -> obj
        const decryptedText = this.CryptoJS.AES.decrypt(dataList[i], this.m_key).toString(this.CryptoJS.enc.Utf8);
        let decrpted_obj = JSON.parse(decryptedText);
        this.dataList.push(decrpted_obj);
      }
         
    },

    addData(){
      const addDataForm = this.$refs.add_data_form.validate();
      console.log(addDataForm);
      if(addDataForm){
        console.log(this.add_data);
        this.generateCrypto(this.add_data, this.m_key, this.user_id);
      }
    },

    async generateCrypto(data, m_key, user_id){
      // add_data -> crytoValue
      const JsonString = JSON.stringify(data);
      console.log(JsonString);
      const encryptedText = this.CryptoJS.AES.encrypt(JsonString, m_key).toString();
      console.log(encryptedText);

      const enc_data = {
        crypto_data: encryptedText,
        user_id:user_id,
        m_key:m_key
      }

      return await this.axios({
        url:"http://localhost:5000/add/crypto_data",
        method: 'POST',
        data: enc_data,

      }).then((res)=>{
          if(res.data.response == "success") {
            this.data_alert_type = "success"
            this.data_alert = true;
            this.data_alert_msg = "Data Added Successfully!"
            this.submit();
          }
          else{
            this.data_alert_type = "error"
            this.data_alert = true;
            this.data_alert_msg = "Error: Failed to add data."
          }
      }) 

    },
    
    hide_alert() {
      window.setInterval(() => {
        this.alert = false;
      }, 5000) 
    },

    hide_data_alert() {
      window.setInterval(() => {
        this.alert = false;
      }, 4000) 
    }
  }

}
</script>
