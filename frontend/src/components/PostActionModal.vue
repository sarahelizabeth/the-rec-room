<template>
  <Transition name="modal">
    <div id="additional-action-modal" :class="{'is-active': show}" class="modal">
      <div class="modal-background"></div>
      <div class="modal-content">
        <div class="box">

          <!-- Modal body -->
          <div class="media">
            <div class="media-left pt-1">
              <span class="icon is-medium">
                <span class="fa-stack fa-sm">
                  <i class="fas fa-circle fa-stack-2x has-text-danger"></i>
                  <slot name="icon"></slot>
                </span>
              </span>
            </div>
            <div class="media-content">
              <p class="title is-size-3 mb-1"><slot name="header"></slot></p>
              <p><slot name="body"></slot></p>
          
              <!-- Modal footer -->
              <div class="field is-grouped mt-4">
                <div class="control is-expanded">
                  <div v-if="actionType == 'deleteAction'">
                    <label class="checkbox">
                      <input type="checkbox" v-model="deleteConfirmation">
                      Yes, I'm sure
                    </label>
                  </div>
                  <div v-else>
                    <input v-model="reportConfirmation" class="input" type="text" placeholder="Reason for report...">
                  </div>
                </div>
                <div class="control">
                  <button @click="$emit('close')" class="button is-light">Cancel</button>
                </div>
                <div class="control">
                  <button v-if="actionType == 'deleteAction'" @click="submitAction" :disabled="!deleteConfirmation" class="button is-danger">Delete</button>
                  <button v-else @click="submitAction" :disabled="reportConfirmation.length === 0" class="button is-danger">Report</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button @click="$emit('close')" class="modal-close is-large" aria-label="close"></button>
    </div>
  </Transition>
</template>

<script>
export default {
  props: {
    show: Boolean,
    actionType: String,
  },
  data() {
    return {
      deleteConfirmation: false,
      reportConfirmation: '',
    }
  },
  methods: {
    submitAction() {
      if (this.actionType == 'deleteAction') {
        this.$emit('submitted')
      } else {
        this.$emit('submitted', this.reportConfirmation)
      }
    },
  },
}
</script>

<style>
/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter-from {
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>