provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_cloud_run_service" "ltm_challenge" {
  name     = "ltm-challenge"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/ltm-challenge"
        resources {
          limits = {
            memory = "2gi"
            cpu = "1"
          }
        }
        ports {
          container_port = "8000"
        }
      }
    }
  }

  traffic {
    percent = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "invoker" {
  service  = "google_cloud_run_service.ltm_challenge.name"
  location = "google_cloud_run_service.ltm_challenge.location"
  role = "roles/run.invoker"
  member = "allUsers"
}






