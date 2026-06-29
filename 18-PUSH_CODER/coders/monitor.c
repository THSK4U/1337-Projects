/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:58:45 by Tsellak           #+#    #+#             */
/*   Updated: 2026/06/29 10:40:46 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	simulation_check(t_data *data)
{
	int	ended;

	pthread_mutex_lock(&data->state_mutex);
	ended = data->simulation_end;
	pthread_mutex_unlock(&data->state_mutex);
	return (ended);
}

int	mark_burnout(t_coder *coder)
{
	int	should_print;

	pthread_mutex_lock(&coder->data->state_mutex);
	should_print = !coder->data->simulation_end;
	if (should_print)
		coder->data->simulation_end = 1;
	pthread_mutex_unlock(&coder->data->state_mutex);
	if (should_print)
		log_action(coder, "burned out");
	return (should_print);
}

static int	check_and_mark(t_data *data)
{
	long	now;
	int		i;
	int		all_done;

	now = get_time_ms();
	all_done = 1;
	i = 0;
	while (i < data->num_coders)
	{
		pthread_mutex_lock(&data->coders[i].state_mutex);
		if (data->coders[i].compile_count < data->num_compiles_required)
		{
			all_done = 0;
			if (now >= data->coders[i].deadline)
				mark_burnout(&data->coders[i]);
		}
		pthread_mutex_unlock(&data->coders[i].state_mutex);
		i++;
	}
	return (all_done);
}

void	*monitor_routine(void *arg)
{
	t_data	*data;

	data = (t_data *)arg;
	while (!simulation_check(data))
	{
		if (check_and_mark(data))
		{
			pthread_mutex_lock(&data->state_mutex);
			data->simulation_end = 1;
			pthread_mutex_unlock(&data->state_mutex);
			break ;
		}
		usleep(1000);
	}
	return (NULL);
}
