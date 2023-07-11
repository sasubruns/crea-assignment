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

For both possible solutions, alert criteria setup by each user should be stored in a database table. Let's imagine a scenario where the user can customize a minimum and maximum shipment size and a destination country that should trigger an alert. The alert criteria table will have the following schema:

```(user_id, min_shipment_size, max_shipment_size, destination)```

Multiple rows per user are possible in case the user wants to setup alerts for multiple different types of shipments.

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

I haven't tested this query in PostgreSQL so it might have some syntax errors, but hopefully the idea is clear enough.