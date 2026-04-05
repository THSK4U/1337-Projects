/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_str.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/14 04:19:39 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/14 16:31:23 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_str(char *str)
{
	size_t	len;

	if (!str)
		return (write(1, "(null)", 6));
	len = 0;
	while (str[len] != '\0')
		len++;
	return (write(1, str, len));
}
