<template>
<div class="register">
  <v-container fluid fill-height>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <h1> User Registeration </h1>
      </v-col>
    </v-row>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="10" md="8" lg="6" >
      <v-card>
        <v-form ref="registerForm">
        <v-card-text>
          <v-text-field ref="username" v-model="username"
            :rules="[() => !!username || 'This field is required']"
            label="Username"  required
          ></v-text-field>
          <v-text-field ref="email" v-model="email"
            :rules="[() => !!email || 'This field is required']"
            label="Email"  required
          ></v-text-field>
          <v-text-field
            ref="password" v-model="password"
            :rules="[() => !!password || 'This field is required']"
            label="Password" required
          ></v-text-field>
        </v-card-text>
        <v-divider class="mt-12"></v-divider>
        <v-card-actions>
          <v-btn text>
            Cancel
          </v-btn>
          <v-spacer></v-spacer>
          <!-- <v-spacer></v-spacer> -->
            <v-dialog v-model="dialog"
            persistent max-width="500"
            >
              <v-card>
                <v-card-title class="text-h5">
                 {{this.dialogTitle}}
                </v-card-title>
                <v-card-text>
                  <h3>{{this.dialogMsg}}</h3>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="toLogin"
                  >
                    OK
                  </v-btn>
                </v-card-actions>
              </v-card>
          </v-dialog>
          <v-btn
            color="primary"
            text
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
        </v-card-actions>
        </v-form>
      </v-card>
      <v-spacer></v-spacer>
      <h5>Already Have an Account? <router-link to="/login">Login Here</router-link></h5>
    </v-col>
  </v-row>
  
  </v-container>
</div>
</template>

<script>
  export default {
    data: () => ({
      
      username:null,
      email:null,
      password:null,
      dialog: false,
      btnloader: false,
      // formHasErrors: false,
      dialogMsg:null,
      dialogTitle:null,

    }),
    computed:{

    },
    methods:{
      async userRegister(url, msg) {
        this.btnloader = true;
        return await this.axios({
          url: url,
          method: 'POST',
          // responseType: 'application/json',
          data: msg,
        }).then((res)=>{
          this.btnloader = false;
          this.dialog = true;
          console.log(res);
          var response = res.data.response;
          console.log(response);
          var msg = res.data.results.message
          if(response == "success"){
            console.log("true");
            var m_key = res.data.results.generated.master_key;
            this.dialogTitle = "Registered Successfully";
            this.dialogMsg = msg + "\nMaster Key : " + m_key;
            console.log(m_key);
            
          }else{
            this.dialogTitle = "Registeration Failed"
            this.dialogMsg = msg;
            console.log(this.dialogMsg);
          }
        })
      },
      async submit(){
        const validateForm = this.$refs.registerForm.validate();
        const msg = {
          username:this.username,
          email:this.email,
          password:this.password
        }
        console.log(validateForm);
        console.log(msg);
        if(validateForm){
          await this.userRegister("http://localhost:5000/user/register", msg);
        }

      },

      toLogin(){
        this.dialog= false,
        this.$router.push({ name: 'Login'});
      },
      
    }
  }

</script>
