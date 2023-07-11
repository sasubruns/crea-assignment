# Task 1: Infrastructure

Solutions/suggestions to the first task are presented in this readme. Instead of presenting a single configuration for each situation, I chose to lay out two possible approaches that could be chosen from depending on priorities.

## Internal monitoring

```In the Russia project, we run processes on a daily basis and need to know whether they have run successfully or not. Please suggest one or several configurations that would allow us (internally) to check the success of each process. We are looking for setups that are both easy to maintain and generate as little friction / efforts as possible for us to check```

### Option 1: Store process logs in a database

The most flexible and lightweight option is to store simplified process logs in a database. Extending the existing API or creating a new dedicated one for receiving process logs should be simple. Internal users can access these logs either from the cloud or a local database client. It was mentioned in the interview that you are already using a PostgreSQL database, which should be a suitable place for these logs. If a more flexible structure is required, a separate NoSQL database could be used. However if the purpose is simply to report something like timestamps, process names, and process states then a relational database will do the job just fine.

Pros:
- Easy to setup
- Easy to maintain

Cons:
- Users need to have the skills and tools to use databases, especially if they are looking for specific process runs from a large amount of data
- This setup is not efficient for storing more detailed information like large error messages or stack traces. This solution is only good for checking the success of each process, not why it failed.
- Each process needs to be modified to report state to the database

### Option 2: Use a dedicated logging and observability tool

For a more user-friendly and feature-rich approach, I would suggest using a dedicated logging and observability tool. Personally I have used a tool called Splunk, but a quick Google search shows many (open-source!) alternatives like SigNoz, Logstash and Fluentd. All of these provide a visual user interface and high customizability. These tools offer multiple ways to receive log data from processes, including e.g. listen servers or polling.

Pros:
- Feature rich
- Friendly for non-tech users
- High level of detail
- Logs can have complex structures

Cons:
- More setup
- More maintenance
- Probably overkill when it comes to features if the goal is to simply monitor whether processes have succeeded or not

## External alerts

```External users of our platform should be able to set alerts for when potential fraudulent shipments are detected. Assuming the shipments are created in bulk and stored in a Postgres database query, design an infrastructure that would allow user to create / edit alert criteria and receive them when our system detects them. Please describe the setup in detail.```

For this problem I'm making the assumption that a front-end UI that enables users to edit criteria is already in place, since this task is about infrastructure. I'm also not very experienced in front-end development, so describing how to build such a UI would require some guesswork on my part. Hopefully you can forgive me.

For both possible solutions, alert criteria that users have setup should be stored in a database table. Let's imagine a scenario where the user can customize a minimum and maximum shipment size and a destination country that should trigger an alert. The alert criteria table will have the following schema:

```(user_id, min_shipment_size, max_shipment_size, destination)```

Multiple rows per user are possible in case the user wants to setup alerts for multiple different types of shipments.

How you want to alert the users is up to you (or them), here are two simple possibilities:

- Email alerts can be sent either with a third-party email service (such as SendGrid, Mailgun or Mailjet) or a custom email server running in the cloud.
- Alerts can be sent to the UI. In this case the alerts need to be stored in the database and the front-end should fetch the alerts for each user whenever it's loaded.

### Option 1: Run batch jobs that send alerts

In this scenario, alerts are triggered by batch jobs that run on a schedule (e.g. every 20 minutes). These jobs will maintain information on which data is new (and thus not yet investigated for alerts) by storing the timestamp of the newest data point in the last batch. Data not yet been received by an alert job will be picked up by the next one.

The job starts by running an SQL query that joins the latest batch with the table containing the alert criteria for each user. If we use the example schema imagined earlier, the SQL query would look something like:

```sql
SELECT criteria.user_id,
    shipments.shipment_id
FROM shipments
INNER JOIN user_alert_criteria AS criteria
ON (
    shipments.destination_country = criteria.destination
    AND shipments.shipment_size BETWEEN criteria.min_shipment_size AND criteria.max_shipment_size
);
```

I haven't tested this query in PostgreSQL so it might have some syntax errors, but hopefully the idea is clear enough. Of course the alert criteria should be much more complex, but this logic is easy to extend for such purposes. After running this query for the latest batch of shipments, the job has received data on which users should be alerted about which shipments, and can simply trigger these alerts or store this data in the database for the front-end.

This batch job is so simple that I imagine it could be run as a small Python script in either a serverless service like Cloud Run (which makes scheduling easy), or a more traditional VM instance (in which case scheduling could be performed using cron or a similar tool). Most ETL tools are also suitable for this job if such tools are already in use in the organization.

Pros:
- Simple infrastructure
- Can easily handle large amounts of both shipments and alert criteria from the get-go since the only performance bottleneck is the SQL join

Cons:
- Alerts are not real time. In the worst scenario the lag for alerts is equal to the time between job runs. Not a very big concern if jobs are scheduled often, e.g. every 15 minutes.

### Option 2: Trigger alert screening from the API

For this option, all shipments should be loaded into the database using the API. Whenever the API receives a new batch of shipments, the batch will be screened for alert criteria matches (in a similar fashion to Option #1) either directly by the API or a separate service/API. This approach is real-time, so users will receive alerts instantly, but the API has to trigger this process for any amount of data it receives, which could increase complexity if data is sent to the API very often.

Pros:
- Instant/real-time alerting
- If the API handles everything, no setup of any separate infrastucture is required

Cons:
- API might get clogged up performance wise, which will decrease it's ability to receive requests and respond to them.
- If the alert screening is delegated to a separate service, setup will be more difficult since essentially a separate API needs to be developed for this task.
